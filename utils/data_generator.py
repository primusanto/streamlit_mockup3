"""
Mock data generation for the dashboard
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from typing import List, Dict
import config

def generate_historical_data(months: int = 24) -> pd.DataFrame:
    """
    Generate comprehensive mock historical data for the dashboard

    Args:
        months: Number of months of historical data to generate

    Returns:
        DataFrame with comprehensive property management data
    """
    np.random.seed(42)
    random.seed(42)

    # Generate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=months * 30)
    date_range = pd.date_range(start=start_date, end=end_date, freq='MS')

    data = []

    for pm in config.PORTFOLIO_MANAGERS:
        agency = random.choice(config.AGENCIES)

        # Generate trend for this PM (some growing, some stable, some declining)
        base_landlords = random.randint(20, 80)
        base_properties = random.randint(50, 300)
        trend = random.choice(['growing', 'stable', 'declining'])

        for i, date in enumerate(date_range):
            # Apply trend
            if trend == 'growing':
                growth_factor = 1 + (i * 0.02)
            elif trend == 'declining':
                growth_factor = 1 - (i * 0.01)
            else:
                growth_factor = 1 + random.uniform(-0.05, 0.05)

            landlords = int(base_landlords * growth_factor) + random.randint(-5, 5)
            properties = int(base_properties * growth_factor) + random.randint(-10, 10)
            leases = int(properties * random.uniform(0.80, 0.95))
            vacancies = properties - leases

            # Revenue calculations
            avg_fee = random.uniform(800, 2500)
            management_fees = leases * avg_fee * random.uniform(0.9, 1.1)
            leasing_fees = vacancies * random.uniform(1000, 5000)
            other_fees = properties * random.uniform(50, 200)
            total_revenue = management_fees + leasing_fees + other_fees

            # Rent roll
            avg_rent_per_lease = random.uniform(1500, 8000)
            rent_roll = leases * avg_rent_per_lease

            # Arrears
            arrears_rate = random.uniform(0.02, 0.08)
            total_arrears = rent_roll * arrears_rate

            # Distribute arrears across buckets
            arrears_0_30 = total_arrears * random.uniform(0.35, 0.45)
            arrears_31_60 = total_arrears * random.uniform(0.25, 0.35)
            arrears_61_90 = total_arrears * random.uniform(0.15, 0.25)
            arrears_90_plus = total_arrears - arrears_0_30 - arrears_31_60 - arrears_61_90

            # Critical dates (upcoming)
            rent_reviews = random.randint(2, 15)
            lease_expiries = random.randint(1, 12)

            # Diary items
            overdue_items = random.randint(5, 30)
            completed_items = random.randint(20, 100)

            data.append({
                'date': date,
                'agency': agency,
                'portfolio_manager': pm,
                'landlords': max(0, landlords),
                'properties': max(0, properties),
                'leases': max(0, leases),
                'vacancies': max(0, vacancies),
                'occupancy_rate': (leases / properties * 100) if properties > 0 else 0,
                'management_fees': management_fees,
                'leasing_fees': leasing_fees,
                'other_fees': other_fees,
                'total_revenue': total_revenue,
                'rent_roll': rent_roll,
                'total_arrears': total_arrears,
                'arrears_0_30': arrears_0_30,
                'arrears_31_60': arrears_31_60,
                'arrears_61_90': arrears_61_90,
                'arrears_90_plus': arrears_90_plus,
                'avg_fee_per_tenancy': management_fees / leases if leases > 0 else 0,
                'rent_reviews_upcoming': rent_reviews,
                'lease_expiries_upcoming': lease_expiries,
                'overdue_diary_items': overdue_items,
                'completed_diary_items': completed_items
            })

    df = pd.DataFrame(data)
    return df

def generate_revenue_breakdown(df: pd.DataFrame, pm_filter: str = "Whole Agency") -> pd.DataFrame:
    """Generate revenue breakdown by account code"""
    if pm_filter != "Whole Agency":
        df = df[df['portfolio_manager'] == pm_filter]

    # Get latest month
    latest_date = df['date'].max()
    latest_data = df[df['date'] == latest_date]

    breakdown_data = []
    for code in config.REVENUE_CODES:
        if code == "Management Fees":
            amount = latest_data['management_fees'].sum()
        elif code == "Leasing Fees":
            amount = latest_data['leasing_fees'].sum()
        else:
            amount = latest_data['other_fees'].sum() / (len(config.REVENUE_CODES) - 2)

        breakdown_data.append({
            'account_code': code,
            'amount': amount
        })

    return pd.DataFrame(breakdown_data)

def generate_top_landlords(df: pd.DataFrame, pm_filter: str = "Whole Agency", limit: int = 10) -> pd.DataFrame:
    """Generate top landlords by revenue"""
    if pm_filter != "Whole Agency":
        df = df[df['portfolio_manager'] == pm_filter]

    # Get latest month
    latest_date = df['date'].max()
    latest_data = df[df['date'] == latest_date]

    # Generate mock landlord data
    landlord_data = []
    total_properties = int(latest_data['properties'].sum())

    # Generate random landlord names
    first_names = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
                   "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
                  "Rodriguez", "Martinez", "Hernandez", "Lopez", "Wilson", "Anderson", "Thomas", "Taylor"]

    num_landlords = min(limit * 3, total_properties)

    for i in range(num_landlords):
        landlord_name = f"{random.choice(first_names)} {random.choice(last_names)}"
        properties = random.randint(1, 15)
        revenue = properties * random.uniform(2000, 10000)

        landlord_data.append({
            'landlord_name': landlord_name,
            'properties': properties,
            'revenue': revenue
        })

    landlords_df = pd.DataFrame(landlord_data)
    landlords_df = landlords_df.sort_values('revenue', ascending=False).head(limit).reset_index(drop=True)

    return landlords_df

def generate_arrears_details(df: pd.DataFrame, pm_filter: str = "Whole Agency", bucket: str = None) -> pd.DataFrame:
    """Generate detailed arrears data for drill-down"""
    if pm_filter != "Whole Agency":
        df = df[df['portfolio_manager'] == pm_filter]

    # Get latest month
    latest_date = df['date'].max()
    latest_data = df[df['date'] == latest_date]

    # Determine bucket amounts
    if bucket:
        if bucket == "0-30":
            total_amount = latest_data['arrears_0_30'].sum()
        elif bucket == "31-60":
            total_amount = latest_data['arrears_31_60'].sum()
        elif bucket == "61-90":
            total_amount = latest_data['arrears_61_90'].sum()
        else:  # 90+
            total_amount = latest_data['arrears_90_plus'].sum()
    else:
        total_amount = latest_data['total_arrears'].sum()

    # Generate mock tenant details
    num_tenants = random.randint(15, 50)
    details = []

    property_types = config.PROPERTY_TYPES
    tenant_types = ["Company A Pty Ltd", "Company B Limited", "Individual Name", "Trust Name", "Partnership"]

    for i in range(num_tenants):
        property_address = f"{random.randint(1, 999)} {random.choice(['Main', 'High', 'King', 'Queen', 'George'])} Street"
        tenant = random.choice(tenant_types).replace("Name", f"Tenant {i+1}")
        property_type = random.choice(property_types)
        amount = (total_amount / num_tenants) * random.uniform(0.5, 1.5)
        days_overdue = random.randint(1, 120) if not bucket else random.randint(*_get_bucket_range(bucket))

        details.append({
            'property_address': property_address,
            'tenant_name': tenant,
            'property_type': property_type,
            'amount_overdue': amount,
            'days_overdue': days_overdue
        })

    details_df = pd.DataFrame(details)
    details_df = details_df.sort_values('amount_overdue', ascending=False).reset_index(drop=True)

    return details_df

def generate_critical_dates_details(df: pd.DataFrame, pm_filter: str = "Whole Agency", event_type: str = "rent_reviews") -> pd.DataFrame:
    """Generate detailed critical dates for drill-down"""
    if pm_filter != "Whole Agency":
        df = df[df['portfolio_manager'] == pm_filter]

    # Generate monthly breakdown for next 12 months
    start_date = datetime.now()
    months = []

    for i in range(12):
        month_date = start_date + timedelta(days=i*30)
        count = random.randint(3, 15)

        months.append({
            'month': month_date.strftime('%b %Y'),
            'month_date': month_date,
            'count': count
        })

    return pd.DataFrame(months)

def generate_diary_items_details(df: pd.DataFrame, pm_filter: str = "Whole Agency", status: str = "overdue") -> pd.DataFrame:
    """Generate detailed diary items for drill-down"""
    if pm_filter != "Whole Agency":
        df = df[df['portfolio_manager'] == pm_filter]

    # Get latest month
    latest_date = df['date'].max()
    latest_data = df[df['date'] == latest_date]

    if status == "overdue":
        total_count = int(latest_data['overdue_diary_items'].sum())
    else:
        total_count = int(latest_data['completed_diary_items'].sum())

    # Generate mock diary items
    items = []

    for i in range(min(total_count, 50)):  # Limit to 50 for display
        item_type = random.choice([t for t in config.DIARY_ITEM_TYPES if t != "All Types"])
        property_address = f"{random.randint(1, 999)} {random.choice(['Main', 'High', 'King', 'Queen', 'George'])} Street"
        due_date = datetime.now() - timedelta(days=random.randint(1, 90)) if status == "overdue" else datetime.now() - timedelta(days=random.randint(1, 30))
        pm = random.choice(config.PORTFOLIO_MANAGERS)

        items.append({
            'item_type': item_type,
            'property_address': property_address,
            'due_date': due_date,
            'portfolio_manager': pm,
            'days_overdue': (datetime.now() - due_date).days if status == "overdue" else 0
        })

    items_df = pd.DataFrame(items)

    if status == "overdue":
        items_df = items_df.sort_values('days_overdue', ascending=False).reset_index(drop=True)
    else:
        items_df = items_df.sort_values('due_date', ascending=False).reset_index(drop=True)

    return items_df

def _get_bucket_range(bucket: str) -> tuple:
    """Get day range for arrears bucket"""
    if bucket == "0-30":
        return (1, 30)
    elif bucket == "31-60":
        return (31, 60)
    elif bucket == "61-90":
        return (61, 90)
    else:  # 90+
        return (91, 365)

def generate_property_list(pm_data: pd.Series, pm_name: str) -> pd.DataFrame:
    """Generate individual property list for a portfolio manager"""
    np.random.seed(hash(pm_name + "_properties") % 10000)

    num_properties = int(pm_data['properties'])
    num_leases = int(pm_data['leases'])

    properties = []
    for i in range(num_properties):
        is_leased = i < num_leases
        property_id = f"PROP-{hash(pm_name + str(i)) % 10000:04d}"

        street_num = random.randint(1, 999)
        street = random.choice(['Main St', 'High St', 'Park Ave', 'Church St', 'King St', 'Queen St', 'Victoria Rd', 'Station Rd', 'Mill Rd', 'George St'])
        suburb = random.choice(['Paddington', 'Newtown', 'Surry Hills', 'Bondi', 'Redfern', 'Glebe', 'Balmain', 'Pyrmont', 'Ultimo', 'Darlinghurst'])

        properties.append({
            'Property ID': property_id,
            'Address': f"{street_num} {street}, {suburb}",
            'Property Type': random.choice(['House', 'Apartment', 'Townhouse', 'Villa']),
            'Bedrooms': random.choice([1, 2, 2, 3, 3, 3, 4, 4, 5]),
            'Status': 'Leased' if is_leased else 'Vacant',
            'Weekly Rent': f"${random.randint(350, 1200)}" if is_leased else '-',
            'Portfolio Manager': pm_name
        })

    return pd.DataFrame(properties)

def generate_lease_list(pm_data: pd.Series, pm_name: str) -> pd.DataFrame:
    """Generate individual lease list for a portfolio manager"""
    np.random.seed(hash(pm_name + "_leases") % 10000)

    num_leases = int(pm_data['leases'])

    leases = []
    for i in range(num_leases):
        property_id = f"PROP-{hash(pm_name + str(i)) % 10000:04d}"
        lease_id = f"LSE-{hash(pm_name + str(i)) % 10000:04d}"

        street_num = random.randint(1, 999)
        street = random.choice(['Main St', 'High St', 'Park Ave', 'Church St', 'King St', 'Queen St', 'Victoria Rd', 'Station Rd', 'Mill Rd', 'George St'])
        suburb = random.choice(['Paddington', 'Newtown', 'Surry Hills', 'Bondi', 'Redfern', 'Glebe', 'Balmain', 'Pyrmont', 'Ultimo', 'Darlinghurst'])

        tenant_first = random.choice(['James', 'Emma', 'Michael', 'Sarah', 'John', 'Lisa', 'David', 'Amy', 'Peter', 'Kate'])
        tenant_last = random.choice(['Smith', 'Jones', 'Williams', 'Brown', 'Davis', 'Wilson', 'Moore', 'Taylor', 'Anderson', 'Thomas'])

        start_date = datetime.now() - timedelta(days=random.randint(30, 730))
        lease_term = random.choice([6, 12, 12, 12, 24])
        end_date = start_date + timedelta(days=lease_term * 30)

        weekly_rent = random.randint(350, 1200)

        leases.append({
            'Lease ID': lease_id,
            'Property ID': property_id,
            'Address': f"{street_num} {street}, {suburb}",
            'Tenant': f"{tenant_first} {tenant_last}",
            'Start Date': start_date.strftime('%d/%m/%Y'),
            'End Date': end_date.strftime('%d/%m/%Y'),
            'Weekly Rent': f"${weekly_rent}",
            'Term (months)': lease_term,
            'Portfolio Manager': pm_name
        })

    return pd.DataFrame(leases)

def generate_rent_reviews_list(pm_data: pd.Series, pm_name: str) -> pd.DataFrame:
    """Generate list of properties with upcoming rent reviews for a portfolio manager"""
    np.random.seed(hash(pm_name + "_rent_reviews") % 10000)

    num_reviews = int(pm_data['rent_reviews_upcoming'])

    reviews = []
    for i in range(num_reviews):
        property_id = f"PROP-{hash(pm_name + 'review' + str(i)) % 10000:04d}"

        street_num = random.randint(1, 999)
        street = random.choice(['Main St', 'High St', 'Park Ave', 'Church St', 'King St', 'Queen St', 'Victoria Rd', 'Station Rd', 'Mill Rd', 'George St'])
        suburb = random.choice(['Paddington', 'Newtown', 'Surry Hills', 'Bondi', 'Redfern', 'Glebe', 'Balmain', 'Pyrmont', 'Ultimo', 'Darlinghurst'])

        tenant_first = random.choice(['James', 'Emma', 'Michael', 'Sarah', 'John', 'Lisa', 'David', 'Amy', 'Peter', 'Kate'])
        tenant_last = random.choice(['Smith', 'Jones', 'Williams', 'Brown', 'Davis', 'Wilson', 'Moore', 'Taylor', 'Anderson', 'Thomas'])

        # Review date within next 90 days
        review_date = datetime.now() + timedelta(days=random.randint(1, 90))

        current_rent = random.randint(350, 1200)
        proposed_rent = int(current_rent * random.uniform(1.03, 1.08))  # 3-8% increase

        reviews.append({
            'Property ID': property_id,
            'Address': f"{street_num} {street}, {suburb}",
            'Tenant': f"{tenant_first} {tenant_last}",
            'Review Date': review_date.strftime('%d/%m/%Y'),
            'Current Rent': f"${current_rent}/week",
            'Proposed Rent': f"${proposed_rent}/week",
            'Increase': f"{((proposed_rent - current_rent) / current_rent * 100):.1f}%",
            'Portfolio Manager': pm_name
        })

    return pd.DataFrame(reviews)

def generate_lease_expiries_list(pm_data: pd.Series, pm_name: str) -> pd.DataFrame:
    """Generate list of leases expiring soon for a portfolio manager"""
    np.random.seed(hash(pm_name + "_expiries") % 10000)

    num_expiries = int(pm_data['lease_expiries_upcoming'])

    expiries = []
    for i in range(num_expiries):
        property_id = f"PROP-{hash(pm_name + 'expiry' + str(i)) % 10000:04d}"
        lease_id = f"LSE-{hash(pm_name + 'expiry' + str(i)) % 10000:04d}"

        street_num = random.randint(1, 999)
        street = random.choice(['Main St', 'High St', 'Park Ave', 'Church St', 'King St', 'Queen St', 'Victoria Rd', 'Station Rd', 'Mill Rd', 'George St'])
        suburb = random.choice(['Paddington', 'Newtown', 'Surry Hills', 'Bondi', 'Redfern', 'Glebe', 'Balmain', 'Pyrmont', 'Ultimo', 'Darlinghurst'])

        tenant_first = random.choice(['James', 'Emma', 'Michael', 'Sarah', 'John', 'Lisa', 'David', 'Amy', 'Peter', 'Kate'])
        tenant_last = random.choice(['Smith', 'Jones', 'Williams', 'Brown', 'Davis', 'Wilson', 'Moore', 'Taylor', 'Anderson', 'Thomas'])

        # Expiry date within next 90 days
        expiry_date = datetime.now() + timedelta(days=random.randint(1, 90))
        days_to_expiry = (expiry_date - datetime.now()).days

        weekly_rent = random.randint(350, 1200)

        expiries.append({
            'Lease ID': lease_id,
            'Property ID': property_id,
            'Address': f"{street_num} {street}, {suburb}",
            'Tenant': f"{tenant_first} {tenant_last}",
            'Expiry Date': expiry_date.strftime('%d/%m/%Y'),
            'Days to Expiry': days_to_expiry,
            'Weekly Rent': f"${weekly_rent}",
            'Portfolio Manager': pm_name
        })

    return pd.DataFrame(expiries)

def generate_diary_items_list(pm_data: pd.Series, pm_name: str, item_type: str = "overdue") -> pd.DataFrame:
    """Generate individual diary items list for a portfolio manager"""
    np.random.seed(hash(pm_name + "_diary_" + item_type) % 10000)

    num_items = int(pm_data['overdue_diary_items'] if item_type == "overdue" else pm_data['completed_diary_items'])

    items = []
    for i in range(num_items):
        item_id = f"DRY-{hash(pm_name + str(i)) % 10000:04d}"

        street_num = random.randint(1, 999)
        street = random.choice(['Main St', 'High St', 'Park Ave', 'Church St', 'King St'])
        suburb = random.choice(['Paddington', 'Newtown', 'Surry Hills', 'Bondi', 'Redfern'])

        task_type = random.choice(['Inspection', 'Maintenance', 'Lease Renewal', 'Rent Review', 'Repairs', 'Follow-up'])
        priority = random.choice(['High', 'Medium', 'Low'])

        if item_type == "overdue":
            due_date = datetime.now() - timedelta(days=random.randint(1, 60))
            days_overdue = (datetime.now() - due_date).days
            status = 'Overdue'
        else:
            due_date = datetime.now() - timedelta(days=random.randint(1, 30))
            days_overdue = 0
            status = 'Completed'

        items.append({
            'Item ID': item_id,
            'Property': f"{street_num} {street}, {suburb}",
            'Task Type': task_type,
            'Priority': priority,
            'Due Date': due_date.strftime('%d/%m/%Y'),
            'Status': status,
            'Days Overdue': days_overdue if item_type == "overdue" else '-',
            'Portfolio Manager': pm_name
        })

    return pd.DataFrame(items)

def generate_landlord_properties(landlord_name: str, num_properties: int) -> pd.DataFrame:
    """Generate individual property list for a landlord"""
    np.random.seed(hash(landlord_name) % 10000)

    properties = []
    for i in range(num_properties):
        is_leased = random.random() > 0.15  # 85% occupancy
        property_id = f"PROP-{hash(landlord_name + str(i)) % 10000:04d}"

        street_num = random.randint(1, 999)
        street = random.choice(['Main St', 'High St', 'Park Ave', 'Church St', 'King St', 'Queen St', 'Victoria Rd', 'Station Rd', 'Mill Rd', 'George St'])
        suburb = random.choice(['Paddington', 'Newtown', 'Surry Hills', 'Bondi', 'Redfern', 'Glebe', 'Balmain', 'Pyrmont', 'Ultimo', 'Darlinghurst'])

        weekly_rent = random.randint(350, 1200) if is_leased else None

        properties.append({
            'Property ID': property_id,
            'Address': f"{street_num} {street}, {suburb}",
            'Property Type': random.choice(['House', 'Apartment', 'Townhouse', 'Villa']),
            'Bedrooms': random.choice([1, 2, 2, 3, 3, 3, 4, 4, 5]),
            'Status': 'Leased' if is_leased else 'Vacant',
            'Weekly Rent': f"${weekly_rent}" if weekly_rent else '-',
            'Landlord': landlord_name
        })

    return pd.DataFrame(properties)
