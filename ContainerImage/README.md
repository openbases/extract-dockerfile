## Example 2: ContainerImage from a Dockerfile

This third example is for a specification that is also not production, but represents
an ContainerImage (ContainerRecipe, call it what you wish!) with the following
organization:

```bash
Thing > CreativeWork > SoftwareSourceCode > ContainerImage
```

Instead of being fully represented in the library here, is represented with the [specification.yml](specification.yml) file here modified from [here](https://raw.githubusercontent.com/openschemas/spec-container/gh-pages/_yaml/ContainerRecipe.yml).

```bash
wget https://raw.githubusercontent.com/openschemas/spec-container/gh-pages/_yaml/ContainerRecipe.yml
```

The example is similar to the first, but also includes properties that are defined here
that are more specific to a Container Recipe. This would be my preference for the fields to 
capture for such an object. See the script [extract.py](extract.py) as an example.

```bash
python extract.py
```

will produce the final output [shown here](). Note that we are using a "human friendly"
Github pages template, meaning the parsed metadata is also shown in the interface!
If you view the source, you will more properly see the embedded code. This is what
the page would see. Importantly, this version shows software requirements (apt 
and pip) from [container-diff](https://github.com/GoogleContainerTools/container-diff)
 that could then be parsed by a search box to make the guts of the image more
 discoverable, and algorithms to group the container recipe based on its dependencies.
