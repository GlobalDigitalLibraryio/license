package io.digitallibrary.license.model

import io.digitallibrary.license.UnitSuite

class LicenseTest extends UnitSuite {

  test("Test that a valid license is OK") {
    val validLicense = License("cc-by-4.0")
    validLicense.id should equal ("CC-BY-4.0")
    validLicense.name should equal ("CC-BY-4.0")
    validLicense.description should equal ("Creative Commons Attribution 4.0 International")
    validLicense.url should equal ("http://creativecommons.org/licenses/by/4.0/legalcode")
  }

  test("that an invalid license throws an exception") {
    intercept[LicenseNotSupportedException](
      License("unknown license")
    ).getMessage should equal ("The license unknown license is not a valid license.")
  }
}
