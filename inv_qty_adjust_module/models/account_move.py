from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = "account.move"
    # Extend the existing account.move model to add a custom field and behavior

    adjusted_total_amount = fields.Monetary(
        string="Adjusted Total",
        help=(
            "Enter the desired invoice total amount including tax. "
            "The system will adjust the quantities of each invoice line so that the "
            "monetary value before tax is distributed equally among the lines. "
            "For example, if you enter 4,600 (with a 15% tax rate), the total amount "
            "before tax becomes 4,000; if there are two invoice lines, each line is assigned "
            "a value of 2,000 before tax."
        ),
        inverse="_set_adjusted_total_amount",
        store=True
    )

    @api.onchange('adjusted_total_amount')
    def _set_adjusted_total_amount(self):
        """
        Adjust the quantities of each invoice line so that the sum of their monetary values
        (before tax) equals the desired invoice total amount (excluding tax).

        The process is as follows:

        1. Compute the total amount before tax using a fixed tax rate.
           total_without_tax = adjusted_total_amount / (1 + tax_rate)

        2. Calculate the monetary value that should be allocated to each invoice line equally.
           value_per_line = total_without_tax / number_of_lines

        3. For each invoice line, compute the new quantity:
           new_quantity = value_per_line / price_unit
           The computed quantity is then rounded to 2 decimal places.
        """
        for move in self:
            # Proceed only if an adjusted total amount is provided and there are invoice lines
            if move.adjusted_total_amount and move.invoice_line_ids:
                # Assume a fixed tax rate of 15%
                tax_rate = 0.15

                # Step 1: Calculate the total amount before tax.
                total_without_tax = move.adjusted_total_amount / (1 + tax_rate)

                # Step 2: Calculate the number of invoice lines and determine the value to be allocated per line.
                num_lines = len(move.invoice_line_ids)
                value_per_line = total_without_tax / num_lines

                # Step 3: Adjust each invoice line's quantity based on its unit price.
                for line in move.invoice_line_ids:
                    if line.price_unit:
                        # Compute the new quantity so that (price_unit * quantity) equals the allocated value.
                        new_quantity = value_per_line / line.price_unit
                        # Round the new quantity to 2 decimal places for consistency.
                        line.quantity = round(new_quantity, 2)
