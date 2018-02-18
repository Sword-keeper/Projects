## usage
``
    flickr = FlickrAPI(key, secret)
    for e in flickr.find_all_from_group('49072725@N00', page='4'):
        # do something
``

you can use _flickr_call_with_driver and _flickr_call to access more official api.

And if you use the api with webdriver, you can use `flickr.die` to terminate.


(there is a simple sample of flickr2mongo code.
