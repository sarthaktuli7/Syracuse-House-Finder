import pandas as pd
import streamlit as st
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.distance import geodesic # More accurate than haversine for short distances

# --- Configuration ---
# Coordinates for Syracuse University (approximate center)
SU_LAT = 43.0381
SU_LON = -76.1320
SU_COORDS = (SU_LAT, SU_LON)

# --- Data Loading and Preprocessing ---
@st.cache_data
def load_and_prepare_data():
    try:
        # Load the corrected CSV file
        # IMPORTANT: Adjust this path if your CSV is NOT in a 'data' subfolder
        df = pd.read_csv("src/syracuse_rental.csv")
        
        # Ensure required columns exist
        required_cols = ['title', 'price', 'beds', 'address', 'lat', 'lon', 'link', 'neighborhood', 'is_furnished']
        for col in required_cols:
            if col not in df.columns:
                st.error(f"Missing required column in CSV: '{col}'. Please check your CSV format.")
                return None
        
        # Ensure data types are correct and handle potential errors
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df['beds'] = pd.to_numeric(df['beds'], errors='coerce').astype('Int64') # Use Int64 for nullable integer
        df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
        df['lon'] = pd.to_numeric(df['lon'], errors='coerce')
        
        # is_furnished should be boolean
        if 'is_furnished' in df.columns:
            df['is_furnished'] = df['is_furnished'].astype(str).str.lower().map({'true': True, 'false': False, '1': True, '0': False})
        else:
            df['is_furnished'] = False # Default to False if column is missing

        # Drop rows with any missing crucial data for map/filters
        df = df.dropna(subset=['price', 'beds', 'lat', 'lon', 'address'])

        # Calculate distance to SU
        df['distance_to_su_miles'] = df.apply(
            lambda row: geodesic((row['lat'], row['lon']), SU_COORDS).miles if pd.notnull(row['lat']) and pd.notnull(row['lon']) else None,
            axis=1
        )
        
        return df
    except FileNotFoundError:
        st.error(f"Error: The file 'data/corrected_csv.csv' was not found. Please ensure it's in the correct 'data' subfolder or adjust the path.")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred during data loading or processing: {str(e)}")
        # If you need full traceback for future debugging, you can temporarily uncomment:
        # import traceback
        # st.exception(e) 
        return None

# --- Main Streamlit App ---
st.set_page_config(layout="wide") # Use wide layout
st.title("Syracuse Rent Analyzer 🏠🗺️")
st.markdown("Explore rental listings around Syracuse, filtered by price, bedrooms, and distance to Syracuse University.")

df = load_and_prepare_data()

if df is not None and not df.empty:
    # --- Filters ---
    st.sidebar.header("Filter Rentals")

    # Price Slider
    min_price_df, max_price_df = int(df['price'].min()), int(df['price'].max())
    price_range = st.sidebar.slider(
        'Price Range ($)',
        min_value=min_price_df,
        max_value=max_price_df,
        value=(min_price_df, min(max_price_df, 3000)) # Default max to something reasonable
    )

    # Bedroom Count Multi-select
    bed_count_options = sorted(df['beds'].dropna().unique().astype(int).tolist())
    if 0 in bed_count_options:
        bed_count_options.remove(0)
        bed_count_options = ['Studio'] + [str(b) for b in bed_count_options]
    else:
        bed_count_options = [str(b) for b in bed_count_options]

    selected_beds_str = st.sidebar.multiselect(
        'Number of Bedrooms',
        options=bed_count_options,
        default=bed_count_options # Select all by default
    )
    selected_beds = []
    if 'Studio' in selected_beds_str:
        selected_beds.append(0)
    selected_beds.extend([int(b) for b in selected_beds_str if b != 'Studio'])

    # Distance to SU Slider
    max_dist_df = df['distance_to_su_miles'].max()
    distance_filter = st.sidebar.slider(
        'Max Distance to SU (miles)',
        min_value=0.0,
        max_value=float(f"{max_dist_df:.1f}"), # Round for slider max value
        value=min(2.0, float(f"{max_dist_df:.1f}")), # Default to 2 miles or max available
        step=0.1
    )

    # Neighborhood Multi-select
    neighborhood_options = sorted(df['neighborhood'].dropna().unique().tolist())
    selected_neighborhoods = st.sidebar.multiselect(
        'Neighborhood',
        options=neighborhood_options,
        default=neighborhood_options
    )

    # Is Furnished Checkbox
    is_furnished_filter = st.sidebar.checkbox('Show only furnished apartments', value=False)

    # --- Apply Filters ---
    filtered_df = df[
        (df['price'] >= price_range[0]) & (df['price'] <= price_range[1]) &
        (df['distance_to_su_miles'] <= distance_filter)
    ]
    
    if selected_beds:
        filtered_df = filtered_df[filtered_df['beds'].isin(selected_beds)]
    
    if selected_neighborhoods:
        filtered_df = filtered_df[filtered_df['neighborhood'].isin(selected_neighborhoods)]

    if is_furnished_filter:
        filtered_df = filtered_df[filtered_df['is_furnished'] == True]

    # --- Display Results ---
    st.subheader("Available Rentals")
    if not filtered_df.empty:
        st.write(f"Displaying {len(filtered_df)} listings.")
        
        col1, col2 = st.columns([2, 1]) # Adjust column ratios for map and table

        with col1:
            st.write("### Map View")
            st.map(filtered_df[['lat', 'lon']].assign(
                size=200, 
                color=[[255, 0, 0, 160]] * len(filtered_df) 
            ))

        with col2:
            st.write("### Filtered Listings Table")
            display_df = filtered_df[[
                'title', 'address', 'price', 'beds', 'neighborhood', 'is_furnished', 'distance_to_su_miles', 'link'
            ]].rename(
                columns={
                    'beds': 'Beds', 'price': 'Price ($)', 'address': 'Address', 
                    'neighborhood': 'Neighborhood', 'is_furnished': 'Furnished', 
                    'distance_to_su_miles': 'Dist to SU (miles)', 'link': 'Link'
                }
            )
            display_df['Dist to SU (miles)'] = display_df['Dist to SU (miles)'].round(1)

            st.dataframe(display_df, height=400, use_container_width=True)

        st.markdown("---")
        st.subheader("Individual Listing Details")
        for index, row in filtered_df.iterrows():
            st.markdown(f"**{row['title']}** | "
                        f"**Address:** {row['address']} | "
                        f"**Price:** ${row['price']} | "
                        f"**Beds:** {row['beds']} | "
                        f"**Neighborhood:** {row['neighborhood']} | "
                        f"**Furnished:** {'Yes' if row['is_furnished'] else 'No'} | "
                        f"**Distance to SU:** {row['distance_to_su_miles']:.1f} miles "
            )
            st.markdown(f"[View Listing]({row['link']})")
            st.markdown("---") 
    else:
        st.warning("No listings match your current filter criteria. Try adjusting the filters.")

else:
    st.warning("Data could not be loaded or is empty after processing. Please check your CSV file and its path.")