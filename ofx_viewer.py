#!/usr/bin/env python3
"""
OFX Viewer - A tool to view and print OFX files from banks
"""

import argparse
import sys
from datetime import datetime
from typing import Optional

try:
    from ofxparse import OfxParser
except ImportError:
    print("Error: ofxparse library not found. Please install it with: pip install ofxparse")
    sys.exit(1)


class OFXViewer:
    """Class to handle viewing and printing OFX files"""
    
    def __init__(self, ofx_file_path: str):
        """
        Initialize OFX Viewer with file path
        
        Args:
            ofx_file_path: Path to the OFX file
        """
        self.ofx_file_path = ofx_file_path
        self.ofx_data = None
        
    def parse(self) -> bool:
        """
        Parse the OFX file
        
        Returns:
            True if parsing successful, False otherwise
        """
        try:
            with open(self.ofx_file_path, 'rb') as fileobj:
                self.ofx_data = OfxParser.parse(fileobj)
            return True
        except FileNotFoundError:
            print(f"Error: File '{self.ofx_file_path}' not found.")
            return False
        except Exception as e:
            print(f"Error parsing OFX file: {e}")
            return False
    
    def view(self) -> None:
        """Display the OFX file contents in a readable format"""
        if not self.ofx_data:
            print("No OFX data loaded. Please parse the file first.")
            return
        
        print("\n" + "="*70)
        print("OFX FILE VIEWER")
        print("="*70)
        
        # Account information
        if hasattr(self.ofx_data, 'account') and self.ofx_data.account:
            account = self.ofx_data.account
            print(f"\nAccount Information:")
            print(f"  Institution: {account.institution.organization if hasattr(account, 'institution') and account.institution else 'N/A'}")
            print(f"  Account ID: {account.account_id if hasattr(account, 'account_id') else 'N/A'}")
            print(f"  Account Type: {account.account_type if hasattr(account, 'account_type') else 'N/A'}")
            print(f"  Routing Number: {account.routing_number if hasattr(account, 'routing_number') else 'N/A'}")
            
            if hasattr(account, 'statement'):
                statement = account.statement
                print(f"\nStatement Period:")
                print(f"  Start Date: {statement.start_date if hasattr(statement, 'start_date') else 'N/A'}")
                print(f"  End Date: {statement.end_date if hasattr(statement, 'end_date') else 'N/A'}")
                print(f"  Balance: {statement.balance if hasattr(statement, 'balance') else 'N/A'}")
                print(f"  Available Balance: {statement.available_balance if hasattr(statement, 'available_balance') else 'N/A'}")
        
        # Transactions
        if hasattr(self.ofx_data, 'account') and self.ofx_data.account and \
           hasattr(self.ofx_data.account, 'statement') and self.ofx_data.account.statement:
            transactions = self.ofx_data.account.statement.transactions
            
            if transactions:
                print(f"\nTransactions ({len(transactions)} total):")
                print("-"*70)
                
                for idx, txn in enumerate(transactions, 1):
                    print(f"\nTransaction #{idx}:")
                    print(f"  Date: {txn.date if hasattr(txn, 'date') else 'N/A'}")
                    print(f"  Type: {txn.type if hasattr(txn, 'type') else 'N/A'}")
                    print(f"  Amount: ${txn.amount if hasattr(txn, 'amount') else 'N/A'}")
                    print(f"  Payee: {txn.payee if hasattr(txn, 'payee') else 'N/A'}")
                    print(f"  Memo: {txn.memo if hasattr(txn, 'memo') else 'N/A'}")
                    if hasattr(txn, 'id'):
                        print(f"  ID: {txn.id}")
            else:
                print("\nNo transactions found in this OFX file.")
        
        print("\n" + "="*70 + "\n")
    
    def print_summary(self) -> None:
        """Print a summary of the OFX file suitable for printing"""
        if not self.ofx_data:
            print("No OFX data loaded. Please parse the file first.")
            return
        
        print("\n" + "="*70)
        print(f"BANK STATEMENT SUMMARY")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)
        
        # Account summary
        if hasattr(self.ofx_data, 'account') and self.ofx_data.account:
            account = self.ofx_data.account
            print(f"\nAccount: {account.account_id if hasattr(account, 'account_id') else 'N/A'}")
            print(f"Type: {account.account_type if hasattr(account, 'account_type') else 'N/A'}")
            
            if hasattr(account, 'statement'):
                statement = account.statement
                print(f"Period: {statement.start_date} to {statement.end_date}")
                print(f"Balance: ${statement.balance}")
                
                transactions = statement.transactions
                if transactions:
                    print(f"\nTransaction Summary:")
                    print(f"  Total Transactions: {len(transactions)}")
                    
                    total_debits = sum(txn.amount for txn in transactions if txn.amount < 0)
                    total_credits = sum(txn.amount for txn in transactions if txn.amount > 0)
                    
                    print(f"  Total Credits: ${total_credits:.2f}")
                    print(f"  Total Debits: ${total_debits:.2f}")
                    print(f"  Net Change: ${(total_credits + total_debits):.2f}")
        
        print("\n" + "="*70 + "\n")


def main():
    """Main entry point for the OFX Viewer CLI"""
    parser = argparse.ArgumentParser(
        description='OFX Viewer - View and print OFX files from banks',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # View OFX file contents
  python ofx_viewer.py statement.ofx
  
  # View with detailed information
  python ofx_viewer.py statement.ofx --view
  
  # Print summary
  python ofx_viewer.py statement.ofx --print
  
  # Both view and print
  python ofx_viewer.py statement.ofx --view --print
        """
    )
    
    parser.add_argument('ofx_file', help='Path to the OFX file')
    parser.add_argument('-v', '--view', action='store_true', 
                       help='View detailed OFX file contents')
    parser.add_argument('-p', '--print', action='store_true',
                       help='Print summary suitable for printing')
    
    args = parser.parse_args()
    
    # If no flags specified, default to view
    if not args.view and not args.print:
        args.view = True
    
    # Create viewer and parse file
    viewer = OFXViewer(args.ofx_file)
    
    if not viewer.parse():
        sys.exit(1)
    
    # Display based on options
    if args.view:
        viewer.view()
    
    if args.print:
        viewer.print_summary()


if __name__ == '__main__':
    main()
