#!/usr/bin/env python

'''
This script will demonstrate how we can extract metadata from a Dockerfile,
and then generate a (html) web template to serve with it so that it is
able to be indexed by Google Datasets (or ideally, similar with the recipe
as a ImageDefinition).

Author: @vsoch
November 6, 2018 (no longer Halloween :( )

This is a "custom" specification (ImageDefinition) that is represented in the 
local file, recipe.yml. It fits into schema.org like this:

    Thing > CreativeWork > SoftwareSourceCode > ImageDefinition

Other suggestions from the OCI Community for fitting names:

    Thing > CreativeWork > SoftwareSourceCode > BuildDefinition
    Thing > CreativeWork > SoftwareSourceCode > BuildInstructions
    Thing > CreativeWork > SoftwareSourceCode > BuildPlan
    Thing > CreativeWork > SoftwareSourceCode > BuildRecipe
    Thing > CreativeWork > SoftwareSourceCode > Configuration
    Thing > CreativeWork > SoftwareSourceCode > ContainerConfig
    Thing > CreativeWork > SoftwareSourceCode > ContainerRecipe

If you want to see the "only production schema.org" example, see
SoftwareSourceCode/extract.py. If you think this categorization is wrong, 
then please speak up! I'll be updating the list here (and the examples that
follow) based on the community feedback. Thanks!

 - https://groups.google.com/a/opencontainers.org/forum/#!topic/dev/vEupyIGtvJs
 - https://github.com/schemaorg/schemaorg/issues/2059#issuecomment-427208907

'''

from schemaorg.main.parse import RecipeParser
from schemaorg.main import Schema

################################################################################
## Example 1: Define Dockerfile with ContainerRecipe
## Thing > CreativeWork > SoftwareSourceCode > ContainerRecipe
################################################################################

import os

# Step 0. Define absolute paths to our Dockerfile, recipe, output

here = os.path.abspath(os.path.dirname(__file__))
recipe_yml = os.path.join(here, "recipe.yml")
index_html = os.path.join(here, "index.html")
spec_yml = os.path.join(here, "specification.yml")
dockerfile = os.path.join(here, "Dockerfile")

# Step 1: Read in the (custom) yaml file as a custom (under development) Schema

containerRecipe = Schema(spec_yml)

# Step 2: Show required and recommended fields from recipe

recipe = RecipeParser(recipe_yml)
print(recipe.loaded)

# Step 3: Extract Container Things! First, the recipe file

from spython.main.parse.parsers import DockerParser
parser = DockerParser(dockerfile).parse()

# See definitions at containerRecipe._properties.keys()

# When you add, they are found at:
# containerRecipe.properties

containerRecipe.add_property('version', containerRecipe.version)
containerRecipe.add_property('environment', parser.environ) # currently a list
containerRecipe.add_property('entrypoint', parser.entrypoint)
containerRecipe.add_property('description', 'A Dockerfile build recipe')

# This would be extracted at build --> push time, so we know the uri.
containerRecipe.add_property('name', "vanessa/sregistry")
containerRecipe.add_property('ContainerImage', parser.fromHeader)


# Step 4: Validate Data Structure

recipe.validate(containerRecipe)

# Step 5, get extra metadata we would get with container-diff!
# Kids don't run command line things from Python at home, it's just bad :)

from schemaorg.utils import run_command
import json

### BELOW should be defined with ContainerImage, as the attributes are from the
# ImageManifest I'm not modeling that here, so we can add them to the example
uri = containerRecipe.properties['name']
response = run_command(['docker', 'pull', uri])    # Pull
response = run_command(['docker', 'inspect', uri]) # Inspect
if response['return_code'] == 0:
    manifest = json.loads(response['message'])[0]
    
# These might be added by the user during Continuous Integration, etc.
license = "https://github.com/singularityhub/sregistry/blob/master/LICENSE"
publication = "http://joss.theoj.org/papers/050362b7e7691d2a5d0ebed8251bc01e"
keywords = "container, containers, singularity, singularity registry"

# Add more (not required) fields - these could be parsed from some yml served with CI
containerRecipe.add_property('operatingSystem', manifest['Os']) 
containerRecipe.add_property('softwareVersion', manifest['Id'])  # shasum
containerRecipe.add_property('identifier', manifest['RepoTags']) # tag
containerRecipe.add_property('url', "https://hub.docker.com/r/vanessa/sregistry") # url
containerRecipe.add_property('alternateName', "Singularity Registry")
containerRecipe.add_property('softwareHelp',"https://singularityhub.github.io/sregistry")
containerRecipe.add_property('citation', publication)
containerRecipe.add_property("license", license)
containerRecipe.add_property("keywords", keywords)

# Note to readers - we can parse an ImageDefinition from a manifest!
# manifest['ContainerConfig'] And it has a name! Hmm.

print("Running container-diff... this might take a minute!")

# Container Diff
response = run_command(["container-diff", "analyze", uri,
                        "--type=pip", "--type=file", "--type=apt", "--type=history",
                        "--json", '--quiet','--verbosity=panic'])

# softwareRequirements
requires = [] # APT and PIP

# note that the top level key here can be history, files, pip, apt, etc.
if response['return_code'] == 0:
    layers = json.loads(response['message'])
    for layer in layers:
        print(layer['AnalyzeType'])

        ## Files
        # This would be where we can do some cool machine learning, but just leave be for now
        if layer['AnalyzeType'] == "File":
            print('Found %s files!' %len(layer['Analysis']))

        ## Pip and Apt will go into softwareRequirements
        if layer['AnalyzeType'] in ["Pip","Apt"]:
            for pkg in layer['Analysis']:
                requires.append('%s > %s==%s' %(layer['AnalyzeType'],
                                                pkg['Name'],
                                                pkg['Version']))         


containerRecipe.add_property("softwareRequirements", requires)

# Found 426 files!
# Here we can go to town parsing the (files) guts to label the container meaningfully
# For now, this example that extracts the software and versions is appropriate.

# Step 6. When above is done, generate json-ld

from schemaorg.templates.google import make_dataset
dataset = make_dataset(containerRecipe, index_html)
print(dataset)
