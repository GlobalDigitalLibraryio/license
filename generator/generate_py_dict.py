#!/usr/bin/env python
# coding:utf-8

import os
import re
from datetime import datetime
import requests
import codecs
import json

licenselist_template = """
#!/usr/bin/env python
# coding:utf-8

\"\"\"
Part of GDL License.
Copyright (C) %YEAR% Global Digital Library

See LICENSE
\"\"\"

# This file is generated from the script generate_py_license.py in https://github.com/GlobalDigitalLibraryio/license/tree/master/generator

license_dict = %SPDX_DEF%

"""


comment_pattern = re.compile(r'\s*#.*$')

script_dir = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.dirname(script_dir)

spdx_license_root = "https://spdx.org/licenses"
spdx_license_url = "{}/licenses.json".format(spdx_license_root)
licenselist_file = os.path.join(project_dir, "generator/licenses.py")


def create_spdx(template):
    response = requests.get(spdx_license_url)
    response.raise_for_status()
    response.encoding = "UTF-8"

    licenses = response.json()["licenses"]
    license_dict = {}
    for license in licenses:
        name = license["name"]
        licenseId = license["licenseId"]
        if len(license["seeAlso"]) == 0:
            continue
        url = license["seeAlso"][0]


        license_dict[licenseId.lower()] = {
            "name": licenseId,
            "description": name,
            "url": url
        }
        


    return template.replace("%SPDX_DEF%", json.dumps(license_dict, sort_keys=True, indent=4))


if __name__ == '__main__':
    with codecs.open(licenselist_file, "w", "utf-8") as f:
        content = create_spdx(licenselist_template)
        with_year = content.replace("%YEAR%", str(datetime.now().year))
        f.write(with_year)
