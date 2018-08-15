#!/usr/bin/env python
# coding:utf-8

import os
import re
from datetime import datetime
import requests
import codecs

licenselist_template = """
/*
 * Part of GDL License.
 * Copyright (C) %YEAR% Global Digital Library
 *
 * See LICENSE
 */

package io.digitallibrary.license.model

object LicenseList {

  sealed abstract class SpdxLicense {
    def licenseId: String
    def name: String
    def reference: String
    def isDeprecatedLicenseId: Boolean
    def isFsfLibre: Boolean
    def detailsUrl: String
    def referenceNumber: String
    def seeAlso: Seq[String]
    def isOsiApproved: Boolean
  }

  private[this] case class SpdxLicenseVal(licenseId: String, name: String, reference: String, isDeprecatedLicenseId: Boolean, isFsfLibre: Boolean, detailsUrl: String, referenceNumber: String, seeAlso: Seq[String], isOsiApproved: Boolean) extends SpdxLicense

  val licenses = Seq(
    %SPDX_DEF%
  )
}

"""


comment_pattern = re.compile(r'\s*#.*$')

script_dir = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.dirname(script_dir)

spdx_license_root = "https://spdx.org/licenses"
spdx_license_url = "{}/licenses.json".format(spdx_license_root)
licenselist_file = os.path.join(project_dir, "src/main/scala/io/digitallibrary/license/model/LicenseList.scala")


def create_spdx(template):
    response = requests.get(spdx_license_url)
    response.raise_for_status()
    response.encoding = "UTF-8"

    licenses = response.json()["licenses"]
    lines = []
    for license in licenses:
        reference = "{}/{}".format(spdx_license_root, license["reference"][2:])
        isDeprecatedLicenseId = license["isDeprecatedLicenseId"]
        isFsfLibre = license["isFsfLibre"] if license.get("isFsfLibre") else "false"
        detailsUrl = license["detailsUrl"]
        referenceNumber = license["referenceNumber"]
        name = license["name"]
        licenseId = license["licenseId"]
        seeAlsoAsList = ['"{}"'.format(n.strip()) for n in license["seeAlso"]]
        seeAlsoSeq = "Seq({})".format(','.join(seeAlsoAsList))

        isOsiApproved = license["isOsiApproved"]

        lines.append(u'License(SpdxLicenseVal("{}", """{}""", "{}", isDeprecatedLicenseId = {}, isFsfLibre = {}, "{}", "{}", {}, isOsiApproved = {}))'.format(
            licenseId,
            name,
            reference,
            "{}".format(isDeprecatedLicenseId).lower(),
            "{}".format(isFsfLibre).lower(),
            detailsUrl,
            referenceNumber,
            seeAlsoSeq,
            "{}".format(isOsiApproved).lower()))


    return template.replace("%SPDX_DEF%", ",\n    ".join(lines))


if __name__ == '__main__':
    with codecs.open(licenselist_file, "w", "utf-8") as f:
        content = create_spdx(licenselist_template)
        with_year = content.replace("%YEAR%", str(datetime.now().year))
        f.write(with_year)
