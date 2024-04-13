import csv
import argparse
import logging
import smtplib
import dns.resolver
import sys

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

def check_mx_record(domain):
    """
    Check if the domain has MX records.
    """
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        return True
    except dns.resolver.NoAnswer:
        return False
    except dns.resolver.NXDOMAIN:
        return False
    except Exception as e:
        logger.error(f"Error checking MX record for domain {domain}: {str(e)}")
        return False

def verify_email_dns(name, email, output_file):
    """
    Verify a single email address using DNS and write result to output CSV file.
    """
    domain = email.split('@')[-1]
    logger.info(f"Processing email using DNS: {name}, {email}")
    mx_valid = check_mx_record(domain)
    validity = 'Valid' if mx_valid else 'Invalid'
    with open(output_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, email, validity])
    logger.info(f"Result written to output file using DNS: {name}, {email}, {validity}")

def verify_email_smtp(name, email, output_file):
    """
    Verify a single email address using SMTP and write result to output CSV file.
    """
    logger.info(f"Processing email using SMTP: {name}, {email}")
    if check_email_address(email):
        # Attempt SMTP verification
        try:
            server = smtplib.SMTP()
            server.set_debuglevel(0)  # Set to 1 for verbose output
            server.connect('mx.example.com')  # Replace with appropriate mail server
            server.verify(email)
            validity = 'Valid'
        except Exception as e:
            logger.error(f"SMTP verification failed for {email}: {str(e)}")
            validity = 'Invalid'
        finally:
            server.quit()
    else:
        validity = 'Invalid'
    
    with open(output_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, email, validity])
    logger.info(f"Result written to output file using SMTP: {name}, {email}, {validity}")

def check_email_address(email):
    """
    Check if the email address is valid.
    """
    return True  # Placeholder for email validation function

def main():
    try:
        parser = argparse.ArgumentParser(description='Verify email addresses from a CSV file via DNS or SMTP.')
        parser.add_argument('-f', '--input_file', type=str, help='Input CSV file path containing email addresses.')
        parser.add_argument('-o', '--output_file', type=str, help='Output CSV file path for storing verification results.')
        parser.add_argument('-m', '--mode', choices=['dns', 'smtp'], default='dns', help='Verification mode: dns or smtp (default: dns)')
        args = parser.parse_args()

        if args.input_file and args.output_file:
            logger.info("##########################################################")
            logger.info("##                                                      ##")
            logger.info("##   BBBBB    OOOO    UU   UU   NN   NN  CCCCC  EEEEE   ##")
            logger.info("##   BB  BB  OO  OO   UU   UU   NNN  NN CC    C EE      ##")
            logger.info("##   BBBBB   OO  OO   UU   UU   NN N NN CC      EEEE    ##")
            logger.info("##   BB  BB  OO  OO   UU   UU   NN  NNN CC    C EE      ##")
            logger.info("##   BBBBB    OOOO     UUUUU    NN   NN  CCCCC  EEEEE   ##")
            logger.info("##                                                      ##")
            logger.info("##                      LESS                            ##")
            logger.info("##               EMAIL VALIDITY CHECK                   ##")
            logger.info("##                                                      ##")
            logger.info("##########################################################")
            logger.info("##                                                      ##")
            logger.info("## Usage example:                                       ##")
            logger.info("## python verify_emails.py -f input.csv -o output.csv   ##")
            logger.info("##                                                      ##")
            logger.info("## Parameters:                                          ##")
            logger.info("## -f, --input_file: Input CSV file path               ##")
            logger.info("## -o, --output_file: Output CSV file path             ##")
            logger.info("## -m, --mode: Verification mode (dns or smtp)         ##")
            logger.info("##                                                      ##")
            logger.info("##########################################################")

            with open(args.input_file, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header if present
                for row_num, row in enumerate(reader, start=1):
                    try:
                        name, email = row
                        if args.mode == 'dns':
                            verify_email_dns(name, email, args.output_file)
                        elif args.mode == 'smtp':
                            verify_email_smtp(name, email, args.output_file)
                        else:
                            logger.error("Invalid verification mode. Please specify 'dns' or 'smtp'.")
                            sys.exit(1)
                    except Exception as e:
                        logger.error(f"Error processing row {row_num}: {str(e)}")

            logger.info("Verification complete. Results written to %s.", args.output_file)
        else:
            logger.error("Please provide both input and output file paths.")
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Script terminated by user (Ctrl + C). Exiting...")
        sys.exit(0)

if __name__ == "__main__":
    main()
