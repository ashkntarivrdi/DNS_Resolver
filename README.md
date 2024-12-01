# DNS Resolver Project

This project implements a custom DNS resolver in Python. It supports handling DNS queries for IPv4 addresses (`A` records) and processes them based on mappings provided in a custom `/etc/myhosts` file. The resolver is capable of handling multiple concurrent requests using threading.

---

## Features
- Handles DNS queries for `A` (IPv4) records.
- Implements custom domain-to-IP resolution using `/etc/myhosts`.
- Supports concurrent request handling using Python threading.

---

## Prerequisites
- Python 3.x
- Ensure `/etc/myhosts` exists and contains valid mappings of domains to IPv4 addresses in the format:
`<IP Address> <Domain>`
Example:

```plaintext    
127.0.0.1 localhost 
8.8.8.8 google.com 
1.1.1.1 cloudflare.com
```
## Running the DNS Resolver


1. Save the resolver script as `dns_resolver.py`.
2. Run the server using the following command:

    ```bash
    python3 dns_resolver.py
4. The DNS server will start and listen on UDP port `5353` by default.


## Testing the Resolver
**Using `dig`**
You can test the DNS resolver using the `dig` command:

    ```bash
    dig @localhost google.com

## Project Structure
    ```bash
    .
    ├── dns_resolver.py    # DNS resolver implementation
    └── README.md          # Project documentation

## Author
**Ashkan Tariverdi**
Student Number: `401105753`

## License
This project is for educational purposes and is not intended for production use. Feel free to modify and extend as needed.
