## Example 1: SoftwareSourceCode from a Dockerfile

Here we can parse a minimal schema.org SoftwareSourceCode from the Dockerfile here:

```bash
python extract.py
```
There is verbose output to the screen about versions and what is going on, but the
resulting data structure is printed last:

```html
<script type="application/ld+json">
{
   "creator":{
      "name":"@vsoch",
      "@type":"Person"
   },
   "version":"3.4",
   "description":"A Dockerfile build recipe",
   "name":"gliderlabs/alpine:3.4",
   "@context":"http://www.schema.org"
}
</script>
```

The information here is minimal as the example is. The idea is that some version of
this metadata to describe the Dockerfile would be included with a webby place that
serves the recipe file.
