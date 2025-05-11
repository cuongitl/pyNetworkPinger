# Ping it  - Network Pinger

A simple command-line tool to ping a single IP address or a range of IP addresses to check their availability.

## Features

- Ping a single IP address.
- Ping a range of IP addresses.
- Display results in a user-friendly format.
- Export data to excel.

## Requirements

- Python 3.x
- Required libraries: `requirements.txt`

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/cuongitl/pingit.git
   cd pingit
   ```

2. Install the required libraries:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Ping a Single IP Address

To ping a single IP address, run the following command:

```bash
python pingit.py <IP_ADDRESS>
```

Replace `<IP_ADDRESS>` with the actual IP address you want to ping.

### Ping a Range of IP Addresses

To ping a range of IP addresses, use the following command:

```bash
python pingit.py <subnet>
```

Replace `<subnet>` with the IP addresses of the range you want to ping.

### Example

To ping a single IP address:

```bash
python pingit.py 192.168.1.1
```

To ping a range of IP addresses from `192.168.1.1/24`

```bash
python pingit.py 192.168.1.0/24
```

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.
