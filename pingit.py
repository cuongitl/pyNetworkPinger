"""
Ping an IP range or single IP.
Packages:
- ping3
- tqdm

"""
import ipaddress
import concurrent.futures
from ping3 import ping, errors
from tqdm import tqdm
import sys
import time


def ping_ip(ip, timeout=3, size=32):
	"""Ping a single IP and return True if alive, False otherwise."""
	ip = str(ip)
	try:
		response = ping(ip, timeout=timeout, size=size)
		
		# Debugging: Print the response to understand what we're getting
		# print(f"Ping response for {ip}: {response}")
		
		# if response is None or False:
		if not response:
			return False
		return True
	except errors.HostUnknown:
		print(f"HostUnknown error for {ip}")
		return False
	except (errors.TimeToLiveExpired,
	        errors.DestinationHostUnreachable,
	        errors.DestinationUnreachable,
	        errors.Timeout,
	        errors.PingError) as e:
		print(f"Error pinging {ip}: {str(e)}")
		return False


def validate_input(subnet):
	"""Validate the input as either a subnet or a single IP address."""
	try:
		# Attempt to create an IPv4Network object
		network = ipaddress.IPv4Network(subnet, strict=False)
		return True, network
	except ValueError:
		try:
			# Attempt to create an IPv4Address object
			ip = ipaddress.IPv4Address(subnet)
			return True, ip
		except ValueError as e:
			return False, str(e)


def check_alive_ips(subnet, max_workers=51):
	"""Check alive IPs in the subnet using multithreading."""
	# Validate the input
	is_valid, result = validate_input(subnet)
	if not is_valid:
		print(f"Invalid input: {result}")
		sys.exit(1)
	
	ips_alive = []
	ips_unreachable = []
	
	if isinstance(result, ipaddress.IPv4Address):
		# If it's a single IP, ping that IP
		if ping_ip(result):
			ips_alive.append(result)
		else:
			ips_unreachable.append(result)
	elif isinstance(result, ipaddress.IPv4Network):
		# If it's a network, ping the range
		try:
			# Get all usable IPs by excluding the first and last IP
			network_usable = list(result.hosts())
		# print(network_usable)
		except ValueError as e:
			print(f"Invalid subnet: {e}")
			return []
		
		ip_list = list(network_usable)
		# Use ThreadPoolExecutor for concurrent pinging
		with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
			# Map ping_ip to all IPs with progress bar
			results = list(tqdm(
				executor.map(ping_ip, ip_list),
				total=len(ip_list),
				desc="Scanning IPs",
				file=sys.stdout
			))
		
		# Collect alive IPs
		for ip, is_alive in zip(ip_list, results):
			if is_alive:
				ips_alive.append(str(ip))
			else:
				ips_unreachable.append(str(ip))
	return ips_alive, ips_unreachable


def cmd(subnet):
	print("=" * 50)
	print(f"Input: {subnet}")
	print("=" * 50)
	ips_alive, ips_unreachable = check_alive_ips(subnet)
	print("=" * 50)
	indentation = "    "
	if len(ips_alive) >= 1:
		print(f"Alive IPs: {len(ips_alive)}")
		for ip in ips_alive:
			print(f"{indentation}Alive IP: {ip}")
		print("=" * 50)
	if len(ips_unreachable) >= 1:
		print(f"Unreachable IPs: {len(ips_unreachable)}")
		for ip in ips_unreachable:
			print(f"{indentation}Unreachable IP: {ip}")
		print("=" * 50)


def howto():
	print()
	print('Usage: pingit.py <subnet or single IP>')
	print()
	print('Example1: pingit.py 172.16.2.0/24')
	print()
	print('Example2: pingit.py 172.16.2.1')
	print()


if __name__ == "__main__":
	if len(sys.argv) < 2:
		howto()
		exit(0)
	start = time.time()
	cmd(sys.argv[1])
	end = time.time()
	
	print(f"Total runtime:{round(end - start, 2)} seconds")

# Example: python pingit.py 172.16.2.0/24
