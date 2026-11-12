import sys
import os
import shutil
from pathlib import Path
from ScriptCollection.GeneralUtilities import GeneralUtilities
from ScriptCollection.TFCPS.DotNet.TFCPS_CodeUnitSpecific_DotNet import TFCPS_CodeUnitSpecific_DotNet_Functions,TFCPS_CodeUnitSpecific_DotNet_CLI


@GeneralUtilities.check_arguments
def update_data_from_submodule(codeunit_folder: str) -> None:
    codeunit_name: str = os.path.basename(codeunit_folder)
    repository_folder = GeneralUtilities.resolve_relative_path("..", codeunit_folder)
    datasubmodule_folder = GeneralUtilities.resolve_relative_path("Other/Resources/Submodules/ip-location-db", repository_folder)
    # "user-country" is used and not "geolite2-country": both have the same format and both are updated regularly,
    # but "user-country" is published under the public-domain-dedication-license (free use without attribution)
    # while the geolite2-data comes with the end-user-license-agreement of MaxMind, which this codeunit would pass
    # on to everybody who uses it, because the file is embedded into the assembly. "user-country" is also the one
    # which the data-source itself recommends for a general application, because it prefers the country of the
    # user over the country of a relay the traffic went through.
    # The ipv4-file is the right one here: the service looks up an address by its first octet, which only exists
    # in an ipv4-address, so a line of the ipv6-file would not even get parsed.
    geo_information_file = GeneralUtilities.resolve_relative_path("user-country/user-country-ipv4.csv", datasubmodule_folder)
    target_folder = GeneralUtilities.resolve_relative_path(f"{codeunit_name}/Data/GeoIPData.csv", codeunit_folder)
    shutil.copyfile(geo_information_file, target_folder)


def update_dependencies():
    current_file = str(Path(__file__).absolute())
    codeunit_folder = GeneralUtilities.resolve_relative_path("../..", current_file)
    tf:TFCPS_CodeUnitSpecific_DotNet_Functions=TFCPS_CodeUnitSpecific_DotNet_CLI.parse(__file__)
    tf.update_dependencies()
    update_data_from_submodule(codeunit_folder)


if __name__ == "__main__":
    update_dependencies()
