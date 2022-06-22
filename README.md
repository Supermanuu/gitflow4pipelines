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
docker compose run -it --rm version-test
```

This will retrieve the version of the application.

To increase the version number of the application you can run the following command:

```
docker compose run -it --rm version-increase-test
```

# Important

To make this work, you need to have a `.env` file in your repo. This will be used to manage the version number.
