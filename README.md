NinjaUri
========

NinjaUri is a simple data retrieval tool for URIs.

[![Build Status: TravisCI](https://travis-ci.org/rovellipaolo/NinjaUri.svg?branch=master)](https://travis-ci.org/rovellipaolo/NinjaUri)
[![Test Coverage: Coveralls](https://coveralls.io/repos/github/rovellipaolo/NinjaUri/badge.svg?branch=master)](https://coveralls.io/github/rovellipaolo/NinjaUri?branch=master)
[![Language Grade: LGTM.com](https://img.shields.io/lgtm/grade/python/g/rovellipaolo/NinjaUri.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/rovellipaolo/NinjaUri/context:python)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

![NinjaUri](docs/images/ninjauri.gif "Screencast of NinjaUri")

## Overview:

NinjaUri uses `pythonwhois-alt` (https://github.com/kilgoretrout1985/pythonwhois-alt) and `tldextract` (https://github.com/john-kurkowski/tldextract) to extract a series of information from a given URI.


## Installation:
The first step is cloning the NinjaUri repository, or downloading its source code.

```
$ git clone https://github.com/rovellipaolo/NinjaUri
$ cd NinjaUri
```

NinjaUri has two ways to be executed, in local environment or in Docker.

### Locally:
To execute NinjaUri in your local machine, you need `Python 3.6` or higher installed.
Just launch the following commands, which will install all the needed Python dependencies and add a `ninjauri` symlink to `/usr/local/bin/`.

```
$ make build
$ make install
```

### Docker:
To execute NinjaUri in Docker, you need `Docker` installed.
To build the Docker image, launch the following command:

```
$ docker build -t ninjauri:latest .
```
Or alternatively:
```
$ make build-docker
```


## Run:
Once you've configured it (see the _"Configuration"_ section), you can run NinjaUri as follows.

### Locally:
To execute NinjaUri in your local machine, launch the following command:

```
$ ninjauri https://en.wikipedia.org/wiki/URI
```
Or alternatively:
```
$ make run uri=https://en.wikipedia.org/wiki/URI
```

This will produce as output a JSON containing all the retrieved data about the given URI.

### Docker:
To execute NinjaUri in Docker, launch the following command:

```
$ docker run --name ninjauri -it --rm ninjauri:latest ninjauri https://en.wikipedia.org/wiki/URI
```
Or alternatively:
```
$ make run-docker uri=https://en.wikipedia.org/wiki/URI
```


## Run checkstyle:
Once you've configured it (see the _"Configuration"_ section), to run the checkstyle execute:
```
$ pylint ninjauri.py
```
Or alternatively:
```
$ make checkstyle
```
**NOTE:** This is using [`pylint`](https://github.com/PyCQA/pylint) under-the-hood.

You can also run the checkstyle automatically at every git commit by launching the following command:
```
$ make install-githooks
```


## Run tests:
Once you've configured it (see the _"Configuration"_ section), you can also run NinjaUri tests as follows.

### Locally:
To run the tests in your local machine, launch the following command:
```
$ python3 -m unittest
```
Or alternatively:
```
$ make test
```

You can also run the tests with coverage by launching the following command:
```
$ make test-coverage
```

### Docker:
To run the tests in Docker, launch the following command:
```
$ docker build -t ninjauri:latest .
$ docker run --name ninjauri --rm -w /opt/NinjaUri ninjauri:latest python3 -m unittest
```
Or alternatively:
```
$ make build-docker
$ make test-docker
```


## Licence:

NinjaUri is licensed under the GNU General Public License v3.0 (http://www.gnu.org/licenses/gpl-3.0.html).


## Sample JSON output

The following is the output of NinjaUri run against a sample URI:
```
$ ninjauri https://en.wikipedia.org/wiki/URI
```
```json
{
    "admin_contacts": {},
    "available": false,
    "billing_contacts": {},
    "create_time": "2001-01-13 00:12:14",
    "domain": "wikipedia.org",
    "domain_id": "D51687756-LROR",
    "expire_time": "2023-01-13 00:12:14",
    "hostname": "en.wikipedia.org",
    "nameservers": [
        "ns0.wikimedia.org",
        "ns1.wikimedia.org",
        "ns2.wikimedia.org"
    ],
    "path": "/wiki/URI",
    "port": "",
    "protocol": "https",
    "query": "",
    "raw": "https://en.wikipedia.org/wiki/URI",
    "registered": true,
    "registrant_contacts": {},
    "registrar": "MarkMonitor Inc.",
    "sld": "wikipedia",
    "status": [
        "clientDeleteProhibited https://icann.org/epp#clientDeleteProhibited",
        "clientTransferProhibited https://icann.org/epp#clientTransferProhibited",
        "clientUpdateProhibited https://icann.org/epp#clientUpdateProhibited"
    ],
    "subdomain": "en",
    "technical_contacts": {},
    "tld": "org",
    "update_time": "2015-12-12 10:16:19",
    "whois": {
        "emails": [
            "abusecomplaints@markmonitor.com"
        ],
        "raw": "Domain Name: WIKIPEDIA.ORG\r\nRegistry Domain ID: D51687756-LROR\r\nRegistrar WHOIS Server: whois.markmonitor.com\r\nRegistrar URL: http://www.markmonitor.com\r\nUpdated Date: 2015-12-12T10:16:19Z\r\nCreation Date: 2001-01-13T00:12:14Z\r\nRegistry Expiry Date: 2023-01-13T00:12:14Z\r\nRegistrar Registration Expiration Date:\r\nRegistrar: MarkMonitor Inc.\r\nRegistrar IANA ID: 292\r\nRegistrar Abuse Contact Email: abusecomplaints@markmonitor.com\r\nRegistrar Abuse Contact Phone: +1.2083895740\r\nReseller:\r\nDomain Status: clientDeleteProhibited https://icann.org/epp#clientDeleteProhibited\r\nDomain Status: clientTransferProhibited https://icann.org/epp#clientTransferProhibited\r\nDomain Status: clientUpdateProhibited https://icann.org/epp#clientUpdateProhibited\r\nRegistrant Organization: Wikimedia Foundation, Inc.\r\nRegistrant State/Province: CA\r\nRegistrant Country: US\r\nName Server: NS0.WIKIMEDIA.ORG\r\nName Server: NS1.WIKIMEDIA.ORG\r\nName Server: NS2.WIKIMEDIA.ORG\r\nDNSSEC: unsigned\r\nURL of the ICANN Whois Inaccuracy Complaint Form https://www.icann.org/wicf/)\r\n>>> Last update of WHOIS database: 2020-05-28T14:27:51Z <<<\r\n\r\nFor more information on Whois status codes, please visit https://icann.org/epp\r\n\r\nAccess to Public Interest Registry WHOIS information is provided to assist persons in determining the contents of a domain name registration record in the Public Interest Registry registry database. The data in this record is provided by Public Interest Registry for informational purposes only, and Public Interest Registry does not guarantee its accuracy. This service is intended only for query-based access. You agree that you will use this data only for lawful purposes and that, under no circumstances will you use this data to (a) allow, enable, or otherwise support the transmission by e-mail, telephone, or facsimile of mass unsolicited, commercial advertising or solicitations to entities other than the data recipient's own existing customers; or (b) enable high volume, automated, electronic processes that send queries or data to the systems of Registry Operator, a Registrar, or Afilias except as reasonably necessary to register domain names or modify existing registrations. All rights reserved. Public Interest Registry reserves the right to modify these terms at any time. By submitting this query, you agree to abide by this policy.\n\nThe Registrar of Record identified in this output may have an RDDS service that can be queried for additional information on how to contact the Registrant, Admin, or Tech contact of the queried domain name.\r\n",
        "servers": [
            "whois.markmonitor.com",
            "whois.pir.org"
        ]
    }
}
```