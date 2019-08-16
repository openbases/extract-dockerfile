# Schema.org Dockerfile Parser

![https://github.com/openschemas/spec-template/raw/master/img/hexagon_square_small.png](https://github.com/openschemas/spec-template/raw/master/img/hexagon_square_small.png)

This is an example of using schema.org to label a Dockerfile. Specifically, we will
walk through examples that use already defined schema.org specifications, and other
examples that use [specifications for containers](https://www.github.com/openschemas/spec-container)
 that are under development. The goal is to demonstrate utility in being able to 
label a Dockerfile (a container recipe) and then different ideas for how this could be done.

## Why should I care?

Labeling our containers and container recipes with schema.org metadata means that
we can serve it alongside the containers, and have the properties indexed by Google Search.
This means that regardless of where your recipe is hosted (a registry or Github pages)
your container and recipes will (finally) be discoverable. Note that the official
definition for a container "recipe" has not been integrated into schema.org, and we
have had [good discussion](https://groups.google.com/a/opencontainers.org/forum/#!topic/dev/vEupyIGtvJs) with the OCI community about a proper name. Any of the
following would be a good contender:

```bash
Thing > CreativeWork > SoftwareSourceCode > BuildDefinition
Thing > CreativeWork > SoftwareSourceCode > BuildInstructions
Thing > CreativeWork > SoftwareSourceCode > BuildPlan
Thing > CreativeWork > SoftwareSourceCode > BuildRecipe
Thing > CreativeWork > SoftwareSourceCode > Configuration
Thing > CreativeWork > SoftwareSourceCode > ContainerConfig
Thing > CreativeWork > SoftwareSourceCode > ImageDefinition
```

Just to provide you with more examples (for the same position in the hierarchy)
I have used several of the names above in the examples below. The only significantly
different is the "SoftwareSourceCode" that cuts away some of the additional recipe
metadata. This is also the only specification that is production schema.org.

## What examples are here?

Toward this goal, we are going to walk through several simple examples 
representing a Dockerfile as each of:

 - [ImageDefinition](ImageDefinition) extraction shown [here](https://openbases.github.io/extract-dockerfile/ImageDefinition/).
 - [ContainerRecipe](ContainerRecipe) extraction shown [here](https://openbases.github.io/extract-dockerfile/ContainerRecipe/).
 - [SoftwareSourceCode](SoftwareSourceCode) extraction shown [here](https://openbases.github.io/extract-dockerfile/SoftwareSourceCode/). This is a specification 
[already defined](https://schema.org/SoftwareSourceCode) in schema.org, 
but does little to describe a Dockerfile in detail.

For each of the above, the metadata shown is also embedded in the page as json-ld
(when you "View Source.") The examples are minimal in that I didn't do any special
parsing of the containers to extract more meaningful tags for software, this would
be valuable to do to improve the search.

Each folder above includes a script to extract (`extract.py`), 
a recipe to follow (`recipe.yml`), and the specification in yaml format (in the 
case of a specification not served by production schema.org). When you view
the [github pages](https://openbases.github.io/extract-dockerfile) of this 
repository served by the master branch, you will see that the `index.html` 
in each folder serves a simple page to show the extracted metadata. The 
[Dockerfile](Dockerfile) is the recipe that we aim to describe using schema.org,
and is for the container [toasterlint/storjshare-cli](https://hub.docker.com/r/toasterlint/storjshare-cli/) on Docker Hub. I chose it pretty randomly because it started with
"toast."


# Usage

Before running these examples, make sure you have installed the module (and note
this module is under development, contributions are welcome!) An install.sh script
is provided that will install Singularity python (spython), Schema Org Python (schemaorg)
along with ContainerDiff.

```bash
$ /bin/bash install.sh
```

For those curious, [ContainerDiff](https://github.com/GoogleContainerTools/container-diff)
allows extraction of different metadata for containers. 
To extract a recipe for a particular datatype, just run the `extract.py` file
in the corresponding folder. You can look at any of the extractors to get a gist
of what we do to generate the final metadata for Github pages. Generally we:

 1. Read in a specific version of the *schemaorg definitions* provided by the library
 2. Read in a *recipe* for a template that we want to populate (e.g., google/dataset)
 3. Use helper functions provided by the template (or our own) to *extract*
 4. Extract, *validate*, and generate the final dataset

The goal of the software is to provide enough structure to help the user (typically a developer)
but not so much as to be annoying to use generally.

## What are the files in each folder?

### recipe.yml Files

If I am a provider of a service and want my users to label their data for my service,
I need to tell them how to do this. I do this by way of a recipe file, in each
example folder there is a file called `recipe.yml` that is a simple listing of required fields defined for the entities that are needed. For example, the [recipe.yml](SoftwareSourceCode/recipe.yml) in the "SoftwareSourceCode" folder tells the parser that we need to define
properties for "SoftwareSourceCode" and an Organization or Person. For example.
with the [schemaorg](https://www.github.com/openschemas/schemaorg) Python module 
I can learn that the "SoftwareSourceCode" definition has 121 properties, 
but the recipe tells us that we only need a subset of those
properties for a valid extraction.

### specification.yml

The specification.yml file is only provided in the [ContainerRecipe](ContainerRecipe)
folder because this isn't a production specification provided by schema.org. For
those that are published (e.g., SoftwareSourceCode and Dataset) the definitions are
provided in the python module.

### extract.py

This is the code snippet that shows how you extract metadata and use the 
[schemaorg](https://www.github.com/openschemas/schemaorg) Python module
to generate the final template page. This file could be run in multiple places!

 - In a continuous integration setup so that each change to master updates the Github Pages metadata.
 - Using a tool like [datalad](https://datalad.org) that allows for version control of such metadata, and definition of extractors (also in Python).
 - As a Github hook (or action) that is run at any stage in the development process.
 - Rendered by a web server that provides Container Recipes for users that should be indexed with Google Search (e.g., Singularity Hub).

Check out any of the subfolders for:

 - [ContainerImage](ContainerImage)
 - [ContainerRecipe](ContainerRecipe)
 - [SoftwareSourceCode](SoftwareSourceCode)

## Resources

 - [Open Container Initative](https://github.com/opencontainers/)
 - [Google Datasets](https://www.blog.google/products/search/making-it-easier-discover-datasets/)
 - [Schemaorg Discussion](https://github.com/schemaorg/schemaorg/issues/2059#issuecomment-427208907)
