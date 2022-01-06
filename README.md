yaml-server
===========

# Scout24 has moved away from using this application. Therefor this applcation is deprecated and the repository will be archived.  

Export a directory of YAML files via HTTP. The YAML files (`*.yaml`) are sorted alphabetically and merged:

* lists get appended
* hashes get merged
* scalars are overwritten

Building
--------

1. Check out the source
1. Build a package 
 1. RPM: Run `python setup.py clean bdist_rpm`, results will be in `dist/`
 1. DEB: Install [python-stdeb](https://pypi.python.org/pypi/stdeb) and run `python setup.py --command-packages=stdeb.command clean bdist_deb`, results will be in `deb_dist`

Configuration
-------------

Configuration happens through a directory of YAML files. The default configuration directory is `/etc/yaml_server` and it contains this content in `00_default.yaml`:

```yaml
#This is the default configuration for yaml_server
#
#Please do not edit this file directly. Create a new file with the settings you want to override
#
# built-in default is 8935, override it if needed
port: 8935
# built-in default is INFO which gives you request logging. Override this with INFO if you really need it. DEBUG is rather chatty.
loglevel: WARNING
#locations:
#   monconf:
#       path: /etc/monconf
#   dummy:
#       path: /dev/null
```

You must add another YAML file next to and define at least one export location. For example create a `10-mydata.yaml` file with the following content:

```yaml
locations:
    mydata:
        path: /etc/mydata
```

This will map HTTP requests to `/mydata` to respond with the merged YAML files from `/etc/mydata`.

Running
-------

To run simply call `yaml_server` and observe the log output in your syslog.
