Note: We will not be updating this application. We switched from raw KVM to Proxmox and this is entirely not needed any longer.

To build:

```
$ docker build -t <tag> .
```

Tag it something memorable. We use `letseatlabs/vmlist`

To run:

```
$ docker run -v $PWD:/opt/app -p 8000:8000 --name vmlist -d <tag>
```

If you update the source code you do not need to rebuild the container, just restart it.

```
$ docker container restart vmlist
```

Screenshot:

![./screenshot.png](https://raw.githubusercontent.com/LetsEatLabs/vmlist/main/screenshot.png)
