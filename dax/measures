**Revenue** = SUM(TransactionSaleAppended[Value])


**Revenue Previous Month** = 
VAR LatestFiscalYear = MAXX(ALL('FiscalYearMonth Table'), 'FiscalYearMonth Table'[Fiscal Year])
VAR LastFiscalMonth = MAXX(
    FILTER(
        ALL('FiscalYearMonth Table'),
        'FiscalYearMonth Table'[Fiscal Year] = LatestFiscalYear
    ),
    'FiscalYearMonth Table'[Fiscal Month]
) - 1 
RETURN
CALCULATE(
    [Revenue],
      REMOVEFILTERS('FiscalYearMonth Table'),
        'FiscalYearMonth Table'[Fiscal Year] = LatestFiscalYear &&
        'FiscalYearMonth Table'[Fiscal Month] = LastFiscalMonth
    )



**YoY Revenue** = 
VAR CurrentFiscalYear = SELECTEDVALUE('FiscalYearMonth Table'[Fiscal Year])
VAR CurrentFiscalMonth = SELECTEDVALUE('FiscalYearMonth Table'[Fiscal Month])
VAR HasMonthFilter = NOT ISBLANK(CurrentFiscalMonth)
VAR LastFiscalYear = CurrentFiscalYear - 1
-- Current Revenue in context
VAR CurrentRevenue = 
    CALCULATE(
        SUM(TransactionSaleAppended[Value])
    )
-- Revenue in same period last year
VAR LastRevenue = 
    CALCULATE(
        SUM(TransactionSaleAppended[Value]),
        FILTER(
            ALL('FiscalYearMonth Table'),
            'FiscalYearMonth Table'[Fiscal Year] = LastFiscalYear &&
            (
                HasMonthFilter = FALSE() ||
                'FiscalYearMonth Table'[Fiscal Month] = CurrentFiscalMonth
            )
        )
    )

RETURN
IF(
    ISBLANK(LastRevenue) || LastRevenue = 0,
    1,  -- 100% increase if no prior year data
    DIVIDE(CurrentRevenue - LastRevenue, LastRevenue)
)


**AvgRevenuePerCustomer** = 
DIVIDE(
    [Revenue],
    DISTINCTCOUNT(TransactionSaleAppended[Customer No])
)


**Purchase Frequency** = 
    COALESCE(
        CALCULATE(
            COUNTROWS(TransactionSaleAppended),
            
            'FiscalYearMonth Table'[Fiscal Year] = MAX('FiscalYearMonth Table'[Fiscal Year]),
            NOT(ISBLANK(TransactionSaleAppended[Value])),
            TransactionSaleAppended[Value] > 0
        ),
        0
    )


**Customer Churn Rate** = 
VAR CurrentFiscalYear = 
    MAX('FiscalYearMonth Table'[Fiscal Year])
VAR PreviousFiscalYear = CurrentFiscalYear - 1
VAR PreviousYearCustomers = 
    CALCULATETABLE(
        VALUES(TransactionSaleAppended[Customer Name]),
        'FiscalYearMonth Table'[Fiscal Year] = PreviousFiscalYear,
        NOT(ISBLANK(TransactionSaleAppended[Value])),  -- Exclude blanks
        TransactionSaleAppended[Value] <> 0            -- Exclude zeros
    )
VAR CurrentYearCustomers = 
    CALCULATETABLE(
        VALUES(TransactionSaleAppended[Customer Name]),
        'FiscalYearMonth Table'[Fiscal Year] = CurrentFiscalYear,
        NOT(ISBLANK(TransactionSaleAppended[Value])),  -- Exclude blanks
        TransactionSaleAppended[Value] <> 0            -- Exclude zeros
    )
VAR LostCustomers = 
    EXCEPT(PreviousYearCustomers, CurrentYearCustomers)
VAR TotalCustomersPreviousYear = 
    COUNTROWS(PreviousYearCustomers)
VAR NumberOfLostCustomers = 
    COUNTROWS(LostCustomers)
RETURN
DIVIDE(NumberOfLostCustomers, TotalCustomersPreviousYear, 0)


**Customer Retention Rate** = 
VAR CurrentFiscalYear = MAX('FiscalYearMonth Table'[Fiscal Year])  -- Respects filter context
VAR PreviousFiscalYear = CurrentFiscalYear - 1
-- Unique customers from the previous fiscal year
VAR PreviousYearCustomers = 
    CALCULATETABLE(
        DISTINCT(TransactionSaleAppended[Customer No]),
        'FiscalYearMonth Table'[Fiscal Year] = PreviousFiscalYear,
        NOT(ISBLANK(TransactionSaleAppended[Value])),  -- Exclude blanks
        TransactionSaleAppended[Value] <> 0            -- Exclude zeros
    )
-- Unique customers from the current fiscal year
VAR CurrentYearCustomers = 
    CALCULATETABLE(
        DISTINCT(TransactionSaleAppended[Customer No]),
        'FiscalYearMonth Table'[Fiscal Year] = CurrentFiscalYear,
        NOT(ISBLANK(TransactionSaleAppended[Value])),  -- Exclude blanks
        TransactionSaleAppended[Value] <> 0            -- Exclude zeros
    )
-- Returning customers (customers present in both years)
VAR ReturningCustomers = 
    INTERSECT(PreviousYearCustomers, CurrentYearCustomers)
-- Count values
VAR ReturningCustomersCount = COUNTROWS(ReturningCustomers)
VAR PreviousYearCustomersCount = COUNTROWS(PreviousYearCustomers)

**Loyal Customers Count** = 
VAR AllCustomers =
    VALUES ( TransactionSaleAppended[Customer Name] )
VAR PastCustomers =
    CALCULATETABLE (
        VALUES ( TransactionSaleAppended[Customer Name] ),
        'FiscalYearMonth Table'[Fiscal Year] < MAX ( 'FiscalYearMonth Table'[Fiscal Year] )
    )
VAR CurrentCustomers =
    CALCULATETABLE (
        VALUES ( TransactionSaleAppended[Customer Name] ),
        'FiscalYearMonth Table'[Fiscal Year] = MAX ( 'FiscalYearMonth Table'[Fiscal Year] )
    )
VAR LoyalCustomers =
    INTERSECT ( PastCustomers, CurrentCustomers )
RETURN
    COUNTROWS ( LoyalCustomers )

**New Customer Count** = 
VAR CurrentFiscalYear = SELECTEDVALUE('FiscalYearMonth Table'[Fiscal Year])
-- Customers from all past years (excluding current year)
VAR AllPastYearsCustomers = 
    CALCULATETABLE(
        VALUES(TransactionSaleAppended[Customer No]),
        'FiscalYearMonth Table'[Fiscal Year] < CurrentFiscalYear,
        NOT(ISBLANK(TransactionSaleAppended[Value])),
        TransactionSaleAppended[Value] > 0 
    )
-- Customers in the current year
VAR CurrentYearCustomers = 
    CALCULATETABLE(
        VALUES(TransactionSaleAppended[Customer No]),
        'FiscalYearMonth Table'[Fiscal Year] = CurrentFiscalYear,
        NOT(ISBLANK(TransactionSaleAppended[Value])),
        TransactionSaleAppended[Value] > 0 
    )
-- Identify New Customers
VAR NewCustomers = 
    EXCEPT(CurrentYearCustomers, AllPastYearsCustomers)
-- Count New Customers
RETURN COUNTROWS(NewCustomers)

**Returned Customer Count** = 
VAR CurrentFiscalYear = SELECTEDVALUE('FiscalYearMonth Table'[Fiscal Year])
VAR PreviousFiscalYear = CurrentFiscalYear - 1
-- Customers who purchased in ANY past year (excluding current year)
VAR AllPastYearsCustomers = 
    CALCULATETABLE(
        VALUES(TransactionSaleAppended[Customer No]),
        'FiscalYearMonth Table'[Fiscal Year] < CurrentFiscalYear,
        NOT(ISBLANK(TransactionSaleAppended[Value])),  -- Exclude blanks
        TransactionSaleAppended[Value] > 0
    )
-- Customers who purchased in the PREVIOUS year
VAR PreviousYearCustomers = 
    CALCULATETABLE(
        VALUES(TransactionSaleAppended[Customer No]),
        'FiscalYearMonth Table'[Fiscal Year] = PreviousFiscalYear,
        NOT(ISBLANK(TransactionSaleAppended[Value])),  -- Exclude blanks
        TransactionSaleAppended[Value] > 0
    )
-- Customers who purchased in the CURRENT year
VAR CurrentYearCustomers = 
    CALCULATETABLE(
        VALUES(TransactionSaleAppended[Customer No]),
        'FiscalYearMonth Table'[Fiscal Year] = CurrentFiscalYear,
        NOT(ISBLANK(TransactionSaleAppended[Value])),  -- Exclude blanks
        TransactionSaleAppended[Value] > 0
    )
-- Identify Comeback Customers
VAR ComebackCustomers = 
    EXCEPT(
        INTERSECT(CurrentYearCustomers, AllPastYearsCustomers),
        PreviousYearCustomers
    )
-- Count Comeback Customers
RETURN COUNTROWS(ComebackCustomers)


**CustomerRank** = 
RANKX(
    ALL(TransactionSaleAppended[Customer Name], TransactionSaleAppended[Customer No], TransactionSaleAppended[Branch Code]),
    CALCULATE(SUM(TransactionSaleAppended[Value])),
    ,
    DESC,
    DENSE
)

**Top10Customers** = 
IF(
    [CustomerRank] <= 10,
    1,
    0
)
