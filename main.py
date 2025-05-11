"""
Packages:
- pyyaml
- pandas
"""
import yaml
import sys
import time
import pandas as pd
from pingit import check_alive_ips

with open("data.yml") as file:
	try:
		subnets = yaml.safe_load(file)
	except yaml.YAMLError as e:
		print(e)
		sys.exit(1)
	except BaseException as e:
		print(e)
		sys.exit(1)


def to_excel(subnet, suffix, data):
	cleaned_ip = subnet.split("/")[0]
	df = pd.DataFrame(data, columns=['ip'])
	# Specify the Excel file and sheet name
	excel_file = f'result/{cleaned_ip}.xlsx'
	sheet_name = f'{cleaned_ip}_{suffix}'
	try:
		# Write the DataFrame to the specified sheet, replacing it if it exists
		with pd.ExcelWriter(excel_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
			df.to_excel(writer, index=False, sheet_name=sheet_name)
		print(f"Data written to '{excel_file}' in sheet '{sheet_name}'.")
	except PermissionError as e:
		print(f"PermissionError: {e}. Please close the Excel file and try again.")
	
	except FileNotFoundError as e:
		print(f"FileNotFoundError: {e}. The file does not exist.")
	
	except Exception as e:
		print(f"An unexpected error occurred: {e}")


def main(subnet, verbose=False):
	start = time.time()
	print(f"Input: {subnet}")
	ips_alive, ips_unreachable = check_alive_ips(subnet)
	print("=" * 50)
	indentation = "    "
	if len(ips_alive) >= 1:
		to_excel(subnet, "alive", ips_alive)
		if verbose:
			print(f"Alive IPs: {len(ips_alive)}")
			for ip in ips_alive:
				print(f"{indentation}Alive IP: {ip}")
	if len(ips_unreachable) >= 1:
		to_excel(subnet, "unreachable", ips_unreachable)
		if verbose:
			print("=" * 50)
			print(f"Unreachable IPs: {len(ips_unreachable)}")
			for ip in ips_unreachable:
				print(f"{indentation}Unreachable IP: {ip}")
	if verbose:
		print("=" * 50)
	end = time.time()
	print(f"Total runtime:{round(end - start, 2)} seconds")


if __name__ == "__main__":
	for subnet in subnets['IPs']:
		main(subnet)
