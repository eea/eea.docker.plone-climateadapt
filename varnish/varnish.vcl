# Marker to tell the VCL compiler that this VCL has been adapted to the
# new 4.0 format.
vcl 4.0;

acl purge {
    "localhost";
    "127.0.0.1";
}

sub vcl_recv {
    # Before anything else we need to fix gzip compression
    if (req.http.Accept-Encoding) {
        if (req.url ~ "\.(jpg|png|gif|gz|tgz|bz2|tbz|mp3|ogg)$") {
            # No point in compressing these
            unset req.http.Accept-Encoding;
        } else if (req.http.Accept-Encoding ~ "gzip") {
            set req.http.Accept-Encoding = "gzip";
        } else if (req.http.Accept-Encoding ~ "deflate") {
            set req.http.Accept-Encoding = "deflate";
        } else {
            # unknown algorithm
            unset req.http.Accept-Encoding;
        }
    }

    if (req.restarts == 0) {
        if (req.http.x-forwarded-for) {
            set req.http.X-Forwarded-For = req.http.X-Forwarded-For + ", " + client.ip;
        } else {
            set req.http.X-Forwarded-For = client.ip;
        }
    }
    if (req.method != "GET" &&
        req.method != "HEAD" &&
        req.method != "PUT" &&
        req.method != "POST" &&
        req.method != "TRACE" &&
        req.method != "OPTIONS" &&
        req.method != "DELETE") {
        /* Non-RFC2616 or CONNECT which is weird. */
        return (pipe);
    }

    if (req.http.X-Forwarded-Proto == "https" ) {
        set req.http.X-Forwarded-Port = "443";
    } else {
        set req.http.X-Forwarded-Port = "90";
        set req.http.X-Forwarded-Proto = "http";
    }

    if (req.method != "GET" && req.method != "HEAD") {
        /* We only deal with GET and HEAD by default */
        # POST - Logins and edits
        if (req.method == "POST") {
            return(pass);
        }

        # PURGE - The CacheFu product can invalidate updated URLs
        if (req.method == "PURGE") {
            if (!client.ip ~ purge) {
                return (synth(405, "Not allowed."));
            }

            # replace normal purge with ban-lurker way - may not work
            # ban ("req.url == " + req.url);
            ban ("obj.http.x-url ~ " + req.url);
            return (synth(200, "Ban added. URL will be purged by lurker"));
        }

        return(pass);
    }

    # cache authenticated requests by adding header
    set req.http.X-Username = "Anonymous";
    if (req.http.Cookie && req.http.Cookie ~ "__ac(|_(name|password|persistent))=")
    {
        set req.http.X-Username = regsub( req.http.Cookie, "^.*?__ac=([^;]*);*.*$", "\1" );

        # pick up a round-robin instance for authenticated users
        set req.backend_hint = cluster_apache.backend();

        # pass (no caching)
        unset req.http.If-Modified-Since;
        return(pass);
    }
    else
    {
        # login form always goes to the reserved instances
        if (req.url ~ "login_form$" || req.url ~ "login$")
        {
            set req.backend_hint = cluster_apache.backend();

            # pass (no caching)
            unset req.http.If-Modified-Since;
            return(pass);
        }
        else
        {
            # downloads go only to these backends
            if (req.url ~ "/(file|download)$" || req.url ~ "/(file|download)\?(.*)")
            {
                set req.backend_hint = cluster_apache.backend();
            }
            else
            {
                # pick up a random instance for anonymous users
                set req.backend_hint = cluster_apache.backend();
            }
        }
    }

    if (req.http.Authorization) {
        /* Not cacheable by default */
        return (pass);
    }

    if (req.method == "GET" && req.http.cookie) {
       return(hash);
    }

    # javascript + css
    if (req.method == "GET" && req.url ~ "\.(js|css)") {
        return(hash);
    }

    ## images
    if (req.method == "GET" && req.url ~ "\.(gif|jpg|jpeg|bmp|png|tiff|tif|ico|img|tga|wmf)$") {
        return(hash);
    }

    ## multimedia
    if (req.method == "GET" && req.url ~ "\.(svg|swf|ico|mp3|mp4|m4a|ogg|mov|avi|wmv)$") {
        return(hash);
    }

    ## xml
    if (req.method == "GET" && req.url ~ "\.(xml)$") {
        return(hash);
    }

    ## for some urls or request we can do a pass here (no caching)
    if (req.method == "GET" && (req.url ~ "aq_parent" || req.url ~ "manage$" || req.url ~ "manage_workspace$" || req.url ~ "manage_main$")) {
        return(pass);
    }

    return (hash);
}

sub vcl_pipe {
    # Note that only the first request to the backend will have
    # X-Forwarded-For set.  If you use X-Forwarded-For and want to
    # have it set for all requests, make sure to have:
    # set bereq.http.connection = "close";
    # here.  It is not set by default as it might break some broken web
    # applications, like IIS with NTLM authentication.
    set req.http.connection = "close";
    return (pipe);
}

sub vcl_backend_response {
    # needed for ban-lurker
    set beresp.http.x-url = bereq.url;

    # Varnish determined the object was not cacheable
    if (!(beresp.ttl > 0s)) {
        set beresp.http.X-Cacheable = "NO: Not Cacheable";
    }

    set beresp.http.X-Backend-Name = beresp.backend.name;
    set beresp.http.X-Backend-IP = beresp.backend.ip;

    set beresp.grace = 30m;

    # cache all XML and RDF objects for 1 day
    if (beresp.http.Content-Type ~ "(text\/xml|application\/xml|application\/atom\+xml|application\/rss\+xml|application\/rdf\+xml)") {
        set beresp.ttl = 1d;
        set beresp.http.X-Varnish-Caching-Rule-Id = "xml-rdf-files";
        set beresp.http.X-Varnish-Header-Set-Id = "cache-in-proxy-24-hours";
    }

    # add Access-Control-Allow-Origin header for webfonts and truetype fonts
    if (beresp.http.Content-Type ~ "(application\/vnd.ms-fontobject|font\/truetype|application\/font-woff|application\/x-font-woff)") {
        set beresp.http.Access-Control-Allow-Origin = "*";
    }

    # intecept 5xx errors here. Better reliability than in Apache
    if ( beresp.status >= 500 && beresp.status <= 505) {
        return (abandon);
    }
}

sub vcl_deliver {
    # needed for ban-lurker, we remove it here
    unset resp.http.x-url;

    # add a note in the header regarding the backend
    set resp.http.X-Backend = req.backend_hint;

    # add more cache control params for authenticated users so browser does NOT cache, also do not cache ourselves
    if (resp.http.X-Backend ~ "auth") {
      set resp.http.Cache-Control = "max-age=0, no-cache, no-store, private, must-revalidate, post-check=0, pre-check=0";
      set resp.http.Pragma = "no-cache";
    }

    if (obj.hits > 0) {
        set resp.http.X-Cache = "HIT";
    } else {
        set resp.http.X-Cache = "MISS";
    }

    unset resp.http.error50x;
}
 
sub vcl_backend_response {
    if (beresp.http.Set-Cookie) {
        return(deliver);
    }

    if (beresp.ttl < 120s) {
        std.log("Adjusting TTL");
        set beresp.ttl = 120s;
    }

    if (beresp.ttl <= 0s || beresp.http.Set-Cookie || beresp.http.Vary == "*") {
        /*
         * Mark as "Hit-For-Pass" for the next 2 minutes
         */
        set beresp.ttl = 120 s;
        set beresp.uncacheable = true;
        # return (hit_for_pass);
        # varnish vcl 4 compat
    }
    return (deliver);
}
 
sub vcl_backend_error {
    if ( beresp.status >= 500 && beresp.status <= 505) {
        # synthetic(std.fileread("/etc/varnish/500msg.html"));
        synthetic("Error varnish test");
    }

    return (deliver);
}
 
sub vcl_synth {
    if (resp.status == 503 && resp.http.X-Backend ~ "auth" && req.method == "GET" && req.restarts < 2) {
      return (restart);
    }

    set resp.http.Content-Type = "text/html; charset=utf-8";

    if ( resp.status >= 500 && resp.status <= 505) {
        synthetic("Error varnish test");
        # synthetic(std.fileread("/etc/varnish/500msg.html"));
    } else {
        synthetic({"
        <?xml version="1.0" encoding="utf-8"?>
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
        <html>
        <head>
        <title>"} + resp.status + " " + resp.http.response + {"</title>
        </head>
        <body>
        <h1>Error "} + resp.status + " " + resp.http.response + {"</h1>
        <p>"} + resp.http.response + {"</p>
        <h3>Guru Meditation:</h3>
        <p>XID: "} + req.xid + {"</p>
        <address>
        <a href="http://www.varnish-cache.org/">Varnish</a>
        </address>
        </body>
        </html>
        "});
    }

    return (deliver);
}
