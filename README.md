# LICENSE
Library for handling licenses in APIs from Global Digital Library.

# Usage
Add dependency to this library: `"gdl" %% "license" % "<version>",`

The main way of using this library is with the case class `License`.
It accepts a string as an identifier for the license

Use SPDX License identifiers. See [https://spdx.org/licenses/](https://spdx.org/licenses/)

A `LicenseNotSupportedException` will be thrown if the string given as input is not a valid license.

Example:

    class MyClass {
       def doSomeLicenseHandling = {
          val license1 = License("CC-BY-4.0")
          val license2 = License("Apache-2.0")
          
          
          println(license1)
          println(license1.description)
          println(license2)
          println(license2.description)
          
       }
    }
    
Output from the above println

    CC-BY-4.0
    Creative Commons Attribution 4.0 International
    Apache-2.0
    Apache License 2.0
 

# Building and distribution

## Updating the library, when standards change

To update this library, run ./generator/generate.py

This will regenerate the content of LicenseList.scala based on the url [https://spdx.org/licenses/licenses.json](https://spdx.org/licenses/)

## Compile
    sbt compile

## Run tests
    sbt test

## Build
    ./build.sh

## Publish
    ./release.sh
