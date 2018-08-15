/*
 * Part of GDL License.
 * Copyright (C) 2018 Global Digital Library
 *
 * See LICENSE
 */

package io.digitallibrary.license.model

import io.digitallibrary.license.model.LicenseList.SpdxLicense


case class License(spdxLicense: SpdxLicense) {
  def id: String = spdxLicense.licenseId
  def name: String = spdxLicense.licenseId
  def description: String = spdxLicense.name
  def url: String = spdxLicense.seeAlso.headOption.getOrElse(spdxLicense.reference)
  override def toString: String = name
}

class LicenseNotSupportedException(message: String) extends RuntimeException(message)

object License {
  def apply(licenseIdentifier: String): License = {
    LicenseList.licenses.find(_.id.equalsIgnoreCase(licenseIdentifier))
      .getOrElse(
        throw new LicenseNotSupportedException(s"The license $licenseIdentifier is not a valid license."))
  }


}
