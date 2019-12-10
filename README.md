# Regestry Image Checker

This is a CLI to access a docker registry using token authorization and check whether an image exists.
It is based on the script provided by [Harbor][1]

## Usage

`./docker-img-check.py <registry/image:tag> <username> <password>`

The `tag` is optional.
If no `tag` is given all tags are listed.

### Return value

`0` is returned if at least one image was found.


[1]: https://github.com/goharbor/harbor/tree/233bbda16c45cc6cb1afd2e5a24ce1219f374392/contrib/registryapi
