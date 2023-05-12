#!/usr/bin/env python3

"""
A simple data retrieval tool for URIs.

:author: Paolo Rovelli
:copyright: GNU General Public License v3.0 (https://www.gnu.org/licenses/gpl.html).
"""

from argparse import ArgumentParser, Namespace, RawTextHelpFormatter
import json
import logging
import sys
from typing import Any, Dict, Optional
from urllib.parse import urlparse
from pythonwhois.net import get_root_server, get_whois_raw
from pythonwhois.parse import parse_raw_whois
from pythonwhois.shared import WhoisException
from tldextract import extract


VERSION = "2.0"


logging.basicConfig(
    format="  >> %(name)s: [%(levelname)s] %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("NinjaUri")


def main():
    args = get_args()
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    try:
        logger.debug(f"Reading target URI '{args.target}'...")
        uri = parse_uri(args.target)
        print_uri(uri, as_json=args.json)
    except (ValueError, WhoisException) as error:
        logger.error(f"Cannot parse target URI: {error}")
        return 1
    return 0


def parse_uri(raw_uri: str) -> Dict:
    uri = {
        "raw": raw_uri,
        "whois": {
            "raw": ""
        }
    }
    parts = get_uri_parts(uri["raw"])
    uri.update(parts)
    domain = get_domain(uri["hostname"])
    uri.update(domain)
    uri["whois"] = get_whois(uri["domain"])
    parse_whois(uri)
    return uri


def get_uri_parts(raw_uri: str) -> Dict:
    logger.debug(f"Parsing URI parts for '{raw_uri}'...")
    info = urlparse(raw_uri)
    logger.debug(f"URI parts: {info}")
    return {
        "hostname": info.netloc if info.netloc != "" else raw_uri,
        "protocol": info.scheme,
        "path": info.path,
        "query": info.query,
        "port": str(info.port) if info.port is not None else ""
    }


def get_domain(hostname: str):
    logger.debug(f"Parsing domain info for '{hostname}'...")
    info = extract(hostname)
    logger.debug(f"Domain info: {info}")
    return {
        "tld": info.suffix,
        "sld": info.domain,
        "domain": info.domain if info.suffix == "" else info.domain + "." + info.suffix,
        "subdomain": info.subdomain
    }


def get_whois(domain: str) -> Dict:
    logger.debug(f"Retrieving Whois info for '{domain}'...")
    raw_whois, servers = get_whois_raw(domain, with_server_list=True)
    whois = {
        "raw": raw_whois[0] if len(raw_whois) > 0 else "",
        "servers": servers
    }
    logger.debug(f'Whois raw info:\n{whois["raw"]}')
    logger.debug(f'Whois servers: {whois["servers"]}')

    logger.debug(f"Retrieving Whois root server for '{domain}'...")
    root_server = get_root_server(domain)
    logger.debug(f"Whois root server: {root_server}")
    if len(whois["servers"]) > 0 and whois["servers"][0] != root_server:
        whois["servers"].insert(0, root_server)

    return whois


def parse_whois(uri: Dict):
    logger.debug("Parsing Whois info for '%s'...", uri["domain"])
    whois = parse_raw_whois(
        [uri["whois"]["raw"]],
        normalized=True,
        never_query_handles=False,
        handle_server=uri["whois"]["servers"][-1]
    )
    logger.debug(f"Whois info:\n{whois}")
    uri["domain_id"] = whois["id"][0] if "id" in whois and len(whois["id"]) > 0 else ""
    uri["status"] = whois["status"] if "status" in whois else []
    if "registrar" in whois and len(whois["registrar"]) > 0:
        uri["registrar"] = whois["registrar"][0]
    else:
        uri["registrar"] = ""
    parse_whois_dates(uri, whois)
    parse_whois_servers(uri, whois)
    parse_whois_contacts(uri, whois)
    parse_whois_status(uri)


def parse_whois_dates(uri: Dict, whois: Dict):
    if "creation_date" in whois and len(whois["creation_date"]) > 0:
        uri["create_time"] = whois["creation_date"][0]
    if "updated_date" in whois and len(whois["updated_date"]) > 0:
        uri["update_time"] = whois["updated_date"][0]
    if "expiration_date" in whois and len(whois["expiration_date"]) > 0:
        uri["expire_time"] = whois["expiration_date"][0]


def parse_whois_servers(uri: Dict, whois: Dict):
    uri["nameservers"] = whois["nameservers"] if "nameservers" in whois else []
    if "whois_server" in whois and len(whois["whois_server"]) > 0:
        uri["whois"]["servers"].insert(0, whois["whois_server"][0])


def parse_whois_contacts(uri: Dict, whois: Dict):
    uri["whois"]["emails"] = whois["emails"] if "emails" in whois else []
    uri["admin_contacts"] = whois["contacts"]["admin"] if whois["contacts"]["admin"] is not None else {}
    uri["billing_contacts"] = whois["contacts"]["billing"] if whois["contacts"]["billing"] is not None else {}
    uri["registrant_contacts"] = whois["contacts"]["registrant"] if whois["contacts"]["registrant"] is not None else {}
    uri["technical_contacts"] = whois["contacts"]["tech"] if whois["contacts"]["tech"] is not None else {}


def parse_whois_status(uri: Dict):
    if uri["whois"]["raw"].startswith("No match for") or len(uri["status"]) == 0:
        uri["available"] = True
        uri["registered"] = False
    else:
        uri["available"] = False
        uri["registered"] = True


def print_uri(uri: Dict, as_json: bool):
    if as_json:
        uri_info = json.dumps(uri, sort_keys=True, ensure_ascii=False, default=str, indent=4)
        print(uri_info)
    else:
        print_uri_info(uri)


def print_uri_info(uri: dict, depth: int = 0):
    for key, value in uri.items():
        if isinstance(value, dict) and value:
            print(format_uri_info(key, None, depth))
            print_uri_info(value, depth + 1)
        elif isinstance(value, list) and len(value) > 0:
            print(format_uri_info(key, None, depth))
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    if index > 0:
                        print("")
                    print_uri_info(item, depth+1)
                elif item:
                    print(format_uri_info(None, item, depth+1))
        elif key != "raw" and value:
            print(format_uri_info(key, value, depth))


def format_uri_info(key: Optional[str], value: Optional[Any], depth: int = 0) -> str:
    if key is None:
        output = "{0} {1}".format(("\t" * depth) + "-", value)
    else:
        key = ("\t" * depth) + key + ":"
        if value is None:
            output = key
        else:
            output = "{0:12} {1}".format(key, value)  # pylint: disable=consider-using-f-string
    return output


def get_args() -> Namespace:
    parser = ArgumentParser(
        description="examples: \n"
                    "  >> %(prog)s target.uri\n"
                    "  >> %(prog)s target.uri --json",
        formatter_class=RawTextHelpFormatter
    )
    parser.add_argument(
        "target",
        metavar="TARGET_URI",
        type=str,
        help="the URI to analyse"
    )
    parser.add_argument(
        "-j",
        "--json",
        action="store_true",
        dest="json",
        help="show the output in JSON format"
    )
    parser.add_argument(
        "-d",
        "--verbose",
        action="store_true",
        dest="verbose",
        help="show verbose logs"
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="NinjaUri " + VERSION,
        help="show version"
    )
    return parser.parse_args()


if __name__ == "__main__":
    sys.exit(main())
