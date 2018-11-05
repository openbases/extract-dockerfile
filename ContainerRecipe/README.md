## Example 2: ContainerRecipe from a Dockerfile

This second example is for a specification that is not production, primarily because
it takes forever and a half to develop a standard. Ain't nobody got time for that.
Thus, the (not production) [ContainerRecipe](https://openschemas.github.io/specifications/ContainerRecipe/)
specification is the following:

```bash
Thing > CreativeWork > SoftwareSourceCode > ContainerRecipe
```

Instead of being fully represented in the library here, is represented with the [specification.yml](ContainerRecipe.yml) file here that was obtained from [here](https://raw.githubusercontent.com/openschemas/spec-container/gh-pages/_yaml/ContainerRecipe.yml).

```bash
wget https://raw.githubusercontent.com/openschemas/spec-container/gh-pages/_yaml/ContainerRecipe.yml
```

The example is similar to the first, but also includes properties that are defined here
that are more specific to a Container Recipe. This would be my preference for the fields to 
capture for such an object. See the script [extract.py] as an example.

```bash
python extract.py
```
```html
<script type="application/ld+json">
{
   "labels":[
      [
         "MAINTAINER",
         "toasterlint \"henry@toasterlint.com"
      ]
   ],
   "environment":[
      "USE_HOSTNAME_SUFFIX=FALSE",
      "DATADIR=/storj",
      "WALLET_ADDRESS=",
      "SHARE_SIZE=1TB",
      "RPCADDRESS=0.0.0.0",
      "RPCPORT=4000"
   ],
   "entrypoint":[
      "[\"/entrypoint\"]"
   ],
   "description":"A Dockerfile build recipe",
   "name":"toasterlint/storjshare-cli",
   "ContainerImage":"gliderlabs/alpine:3.4",
   "operatingSystem":"linux",
   "softwareVersion":"sha256:04ce81ba384870f84ccb5abf8a76a926055f6f781fa82729f810878ec59919fa",
   "identifier":[
      "toasterlint/storjshare-cli:latest"
   ],
   "@context":"http://www.schema.org"
}
</script>
```

The above is missing the most important part - extraction of the softwareRequirements!
See the [ImageDefinition](../ImageDefinition) for an example of doing this.
