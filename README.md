# Introduction 

This is a container that retrieves the version of a certain application and provides a method to increase that version number in one.

# Getting Started

To build the application you need to run the following command:

```
docker compose build
```

This will generate the container into your host. This is not necessary because you can just download the latest version using the next commands.

# Test

To test the application you can run the following command:

```
docker compose run -it --rm test
```

TODO:
Prior to use the test services, you should first set the `PRIVATE_KEY` environment variable with:

```
export PRIVATE_KEY="<private key value>"
```

For example:

```
export PRIVATE_KEY="$(cat ~/.ssh/id_rsa)"
```
