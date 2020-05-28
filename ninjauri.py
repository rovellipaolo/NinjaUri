#!/usr/bin/env python3

"""
A simple data retrieval tool for URIs.

:author: Paolo Rovelli
:copyright: GNU General Public License v3.0 (https://www.gnu.org/licenses/gpl.html).
"""

from argparse import ArgumentParser, Namespace, RawTextHelpFormatter
import json
import logging
from pythonwhois.net import get_root_server, get_whois_raw
from pythonwhois.parse import parse_raw_whois
from pythonwhois.shared import WhoisException
import sys
from tldextract import extract
from typing import Dict, List, Tuple
from urllib.parse import urlparse


VERSION = "1.0"


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
        logger.debug("Reading target URI '%s'...", args.target)
        uri = parse_target_uri(args.target)
    except (ValueError, WhoisException) as e:
        logger.error("Cannot parse target URI: %s", e)
        sys.exit(1)
    print_uri_info(uri)


def get_args() -> Namespace:
    parser = ArgumentParser(
        description="examples: \n"
                    "  >> %(prog)s target.uri\n"
                    "  >> %(prog)s --version\n"
                    "  >> %(prog)s --help",
        formatter_class=RawTextHelpFormatter
    )
    parser.add_argument(
        "target",
        metavar="TARGET_URI",
        type=str,
        help="The targeted URI to analyse."
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        dest="verbose",
        help="Show verbose logs."
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version="NinjaUri " + VERSION,
        help="Show version information."
    )
    return parser.parse_args()


def parse_target_uri(raw_uri: str) -> Dict:
    uri = {
        "raw": raw_uri,
        "whois": {
            "raw": ""
        }
    }
    parse_uri_parts(uri)
    parse_domain(uri)
    uri["whois"]["raw"], uri["whois"]["servers"] = get_whois(uri["domain"])
    root_server = get_whois_root_server(uri["domain"])
    if len(uri["whois"]["servers"]) > 0 and uri["whois"]["servers"][0] != root_server:
        uri["whois"]["servers"].insert(0, root_server)
    parse_whois(uri)
    return uri


def parse_uri_parts(uri: Dict):
    logger.debug("Parsing URI parts for '%s'...", uri["raw"])
    info = urlparse(uri["raw"])
    logger.debug("URI parts: %s", info)
    uri["hostname"] = info.netloc if info.netloc != "" else uri["raw"]
    uri["protocol"] = info.scheme
    uri["path"] = info.path
    uri["query"] = info.query
    uri["port"] = str(info.port) if info.port is not None else ""


def parse_domain(uri: Dict):
    logger.debug("Parsing domain info for '%s'...", uri["hostname"])
    info = extract(uri["hostname"])
    logger.debug("Domain info: %s", info)
    uri["tld"] = info.suffix
    uri["sld"] = info.domain
    uri["domain"] = info.domain if info.suffix == "" else info.domain + "." + info.suffix
    uri["subdomain"] = info.subdomain


def get_whois_root_server(domain: str) -> str:
    logger.debug("Retrieving Whois root server for '%s'...", domain)
    server = get_root_server(domain)
    logger.debug("Whois root server: %s", server)
    return server


def get_whois(domain: str) -> Tuple[str, List[str]]:
    logger.debug("Retrieving Whois info for '%s'...", domain)
    whois, servers = get_whois_raw(domain, with_server_list=True)
    whois = whois[0] if len(whois) > 0 else ""
    logger.debug("Whois raw info:\n%s", whois)
    logger.debug("Whois servers: %s", servers)
    return whois, servers


def parse_whois(uri: Dict):
    logger.debug("Parsing Whois info for '%s'...", uri["domain"])
    whois = parse_raw_whois(
        [uri["whois"]["raw"]],
        normalized=True,
        never_query_handles=False,
        handle_server=uri["whois"]["servers"][-1]
    )
    logger.debug("Whois info:\n%s", whois)
    uri["domain_id"] = whois["id"][0] if "id" in whois and len(whois["id"]) > 0 else ""
    uri["status"] = whois["status"] if "status" in whois else []
    if "registrar" in whois is not None and len(whois["registrar"]) > 0:
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
    uri["nameservers"] = whois["nameservers"] if "nameservers" in whois else[]
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


def print_uri_info(uri: Dict):
    uri_info = json.dumps(uri, sort_keys=True, ensure_ascii=False, default=str, indent=4)
    print(uri_info)


if __name__ == "__main__":
    sys.exit(main())
