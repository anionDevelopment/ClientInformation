---
name: product-knowledge
description: What ClientInformation is, how this repository is structured and which mechanisms exist for building and testing it. Use this before fixing a defect or developing a feature in this repository, to know where things belong and how to verify a change.
---

# ClientInformation

ClientInformation is a service which tells a http-client something about itself, for example the country its
ip-address belongs to.

One property shapes the whole product: **it answers out of data which it carries itself.** There is no request
to a geo-ip-service at runtime, so the service works without internet-access and no address of a user leaves
the machine.

## Structure of the repository

The repository follows the "common project structure": all sourcecode lives in code-units, and every code-unit
has its own `Other`-folder with its build-, quality-check- and reference-files. Use the
`work-with-common-project-structure`-skill when you need the details of that structure.

The code-units are:

- `ClientInformationLibrary` — the lookup itself, including the data. It is usable without the service.
- `ClientInformationBackend` — the dotnet-api-server around the library.
- `ClientInformation` — the application-image of the backend.

## The geo-ip-data

The data comes from the submodule `Other/Resources/Submodules/ip-location-db` and is copied into the library by
`ClientInformationLibrary/Other/UpdateDependencies.py`, which embeds it as `Data/GeoIPData.csv`.

Two things about that file are easy to get wrong:

- **Which source.** `user-country` is used and not `geolite2-country`: both have the same format, but
  `user-country` is published under the public-domain-dedication-license (free use without attribution), while
  the geolite2-data comes with the end-user-license-agreement of MaxMind — and this codeunit passes whatever it
  embeds on to everybody who uses it.
- **Which file.** The ipv4-file is the right one: the lookup finds an address by its first octet, which only
  exists in an ipv4-address, so a line of the ipv6-file would not even be parsed.

`Other/Scripts/UpdateDependencies.py` writes the date of the submodule-commit into the `ReadMe.md`. That date
is the one of the commit in its own timezone (the upstream commits in utc), so it does not change depending on
who runs the script or in which timezone.

## Building

`scbuildcodeunits` builds everything: compile, tests, linting, security-checks, the image and the verification
of the image. The task `task bb` (`BaseBuildAllCodeunits`) does the same.

For a single code-unit, run the scripts in `<code-unit>/Other/Build` and `<code-unit>/Other/QualityCheck`, and
run them from the folder they are located in.
