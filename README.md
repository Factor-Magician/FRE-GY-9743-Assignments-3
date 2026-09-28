# FRE-GY-9743-Assignments-2026fall
Assignments for NYU, FRE-GY 9743, Fall 2026.

## HW3: atomic products and the Visitor pattern

The cashflow classes in `fixedincomelib/product/linear_products.py` follow:

```text
Product
└── ProductCashflow
    ├── ProductFixedAccruedCashflow
    └── ProductOvernightIndexCashflow
```

`Product` and `ProductCashflow` are abstract. `ProductCashflow` initializes
currency, signed notional, direction and payment date. Each concrete product
represents one cashflow building block; a visitor collects its display fields.

Complete the six `#TODO` blocks in `fixedincomelib/product/linear_products.py`
and `fixedincomelib/product/product_display_visitor.py`, then run the notebook.
The base classes, APIs and date helpers are provided.

### Public API

Run `hw3_products.ipynb` from the project root with a Python 3.11 environment
containing the `requirements.txt` dependencies, or use:

```python
from fixedincomelib import (
    qfCreateProductFixedAccruedCashflow,
    qfCreateProductOvernightIndexCashflow,
    qfDisplayProduct,
)

fixed = qfCreateProductFixedAccruedCashflow(
    effective_date="2026-01-02",
    termination_date="2026-04-02",
    currency="USD",
    notional=1_000_000,
    accrual_basis="ACT/360",
    payment_date="2026-04-06",
)

overnight = qfCreateProductOvernightIndexCashflow(
    effective_date="2026-01-02",
    term_or_termination_date="3M",  # also accepts "2026-04-02"
    overnight_index="SOFR-1B",
    notional=-1_000_000,
    compounding_method="compound",
    spread=0.001,  # 10 basis points
    payment_date="2026-04-06",
)

print(qfDisplayProduct(fixed))
print(qfDisplayProduct(overnight))
assert fixed.accrued == 0.25
```

Both creation APIs return product objects. `qfDisplayProduct` returns a
10-row DataFrame with columns `Name` and `Value`.

### Visitor pattern

Read the course tutorial: [IV. Visitor Pattern](https://immense-chocolate-92e.notion.site/IV-Visitor-Pattern-2d4831d0b1d58191bc36ebae3d771d58).

A visitor adds an operation without changing the product classes. Display uses:

```text
qfDisplayProduct(product)
  → product.accept(visitor)
    → visitor.visit(product)
  → visitor.display()
```

`singledispatchmethod` selects the handler registered for the product type.

### Contract fields

| Product | Fields |
|---|---|
| Both | Currency, signed notional, long/short direction, payment date, first/last date |
| Fixed accrued | Effective date, termination date, accrual basis, business-day convention, holiday convention, computed year fraction |
| Overnight index | Effective date, termination date or tenor, index, compounding method, spread; currency comes from the index |

- Fixed `accrued` is a year fraction; this class has no `fixed_rate` field.
  In the example, 90 days / 360 gives 0.25 independently of notional.
- Negative notional implies `SHORT`; zero and positive notional imply `LONG`.
- An omitted, empty or `None` payment date defaults to termination date.
  An explicit payment date is stored separately from the accrual interval.
- Fixed accrual defaults to `F` and `USGS`. The date helper adjusts the accrual
  end for the calculation while preserving the stored contractual dates.
  Use `business_day_convention="NONE"` for no end adjustment.
- For overnight cashflows, explicit termination dates are retained. A tenor is
  advanced with the index's fixing calendar and business-day convention.
- Supported indices are `SOFR-1B` (USD), `FF-1B` (USD) and `SONIA-1B` (GBP),
  case-insensitively.
- Compounding labels are `simple`, `arithmetic` and `compound`; spread is an
  annual decimal rate. These are contract fields; creation and display do not price the cashflow.
- `serialize()` / `deserialize()` convert between products and dictionaries.
