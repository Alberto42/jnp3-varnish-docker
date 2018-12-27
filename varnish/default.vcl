vcl 4.0;

import directors;

backend web { .host = "web"; .port = "8000"; }
backend web2 { .host = "web2"; .port = "8000"; }


sub vcl_init {

    // set up a round-robin director with two backends
    new round_robin_director = directors.round_robin();
    round_robin_director.add_backend(web);
    round_robin_director.add_backend(web2);
}

sub vcl_recv {
    return (hash);
}

sub vcl_backend_fetch {

    // pick one healthy backend from the director
    set bereq.backend = round_robin_director.backend();
}

sub vcl_deliver {

    // disable further caching by downstreams and the client
    set resp.http.Cache-Control = "private, max-age=0, no-store, no-cache, must-revalidate";
}