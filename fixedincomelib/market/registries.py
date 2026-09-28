"""Look up overnight indices without a forecasting curve."""

import QuantLib as ql

__all__ = ["IndexRegistry"]


class IndexRegistry:
    _constructors = {
        "SOFR-1B": ql.Sofr,
        "FF-1B": ql.FedFunds,
        "SONIA-1B": ql.Sonia,
    }

    def get(self, key: str) -> ql.OvernightIndex:
        if not isinstance(key, str):
            raise TypeError("Index name must be a string")
        try:
            constructor = self._constructors[key.upper()]
        except KeyError:
            supported = ", ".join(self._constructors)
            raise ValueError(f"Unknown overnight index {key!r}; supported: {supported}") from None
        return constructor()
