import argparse
import database
import pattern

def main():
    parser = argparse.ArgumentParser(description="Pants Pattern Generator")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- Init DB Command ---
    parser_initdb = subparsers.add_parser("initdb", help="Initialize the database")

    # --- Add Customer Command ---
    parser_add = subparsers.add_parser("add", help="Add a new customer")
    parser_add.add_argument("name", help="Customer's name")
    parser_add.add_argument("address", help="Customer's address")
    parser_add.add_argument("phone", help="Customer's phone number")
    parser_add.add_argument("--length", type=float, default=35, help="Pant Length (inch)")
    parser_add.add_argument("--waist", type=float, default=38, help="Round Waist (inch)")
    parser_add.add_argument("--hip_height", type=float, default=9, help="Hip Height (inch)")
    parser_add.add_argument("--round_hip", type=float, default=47, help="Round Hip (inch)")
    parser_add.add_argument("--thigh", type=float, default=26, help="Round Thigh (inch)")
    parser_add.add_argument("--ankle", type=float, default=14, help="Round Ankle (inch)")

    # --- List Customers Command ---
    parser_list = subparsers.add_parser("list", help="List all customers")

    # --- Generate Pattern Command ---
    parser_generate = subparsers.add_parser("generate", help="Generate a pattern for a customer")
    parser_generate.add_argument("name", help="Name of the customer to generate the pattern for")

    args = parser.parse_args()

    if args.command == "initdb":
        database.init_db()
        print("Database initialized.")
    elif args.command == "add":
        database.add_customer(
            args.name, args.address, args.phone, args.length, args.waist,
            args.hip_height, args.round_hip, args.thigh, args.ankle
        )
    elif args.command == "list":
        customers = database.get_all_customers()
        if customers:
            print("Customers:")
            for customer in customers:
                print(f"  - ID: {customer['id']}, Name: {customer['name']}")
        else:
            print("No customers found.")
    elif args.command == "generate":
        customer = database.get_customer_by_name(args.name)
        if customer:
            pattern.generate_pattern(
                customer['length'], customer['waist'], customer['hip_height'],
                customer['round_hip'], customer['thigh'], customer['ankle'],
                customer['name']
            )
        else:
            print(f"Customer '{args.name}' not found.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
