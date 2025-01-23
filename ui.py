
import pandas as pd
import streamlit as st
from dataplot import read_log_file, filter_logs, plot_combined_access_data
from airesponses import readai, filterai, analyze_ai, concerning_hours, concerning_websites, summary_preferences

log_file_path = "filtered_ftl_log_2025-01-04.txt"
logs = readai(log_file_path)  

        # concerns
filtered_logs = filterai(logs, concerning_websites, concerning_hours)

        # Debug
if filtered_logs:
    result = analyze_ai(filtered_logs)
# Main ui
def main():
    st.title("Network Data")
    st.write("built by isaac")

    # File selection
    log_file_path = "filtered_ftl_log_2025-01-04.txt" 
    websites = ["tiktok.com", "instagram.com", "youtube.com"]
    ip_address = "192.168.0.137"

    # Process logs
    try:
        logs = read_log_file(log_file_path)
        access_counts = filter_logs(logs, websites, ip_address)

        # Plot data
        st.write("### Visits per Hour Plot:")
        plot = plot_combined_access_data(access_counts)
        st.pyplot(plot)

        # sort button
        sort_by = st.radio(
            "Sort data by:",
            ("Hour (Ascending)", "Visits (Descending)"),
            index=1
        )

        # Create columns to see all the tables
        num_websites = len(websites)
        columns = st.columns(num_websites)

        # Display separate tables for each website in columns
        for i, (website, counts) in enumerate(access_counts.items()):
            with columns[i]:
                st.write(f"### {website.capitalize()}")
                raw_data = [{"Hour": hour, "Visits": count} for hour, count in enumerate(counts)]
                raw_data_df = pd.DataFrame(raw_data)

                # Sort with buttons
                if sort_by == "Hour (Ascending)":
                    raw_data_df = raw_data_df.sort_values(by="Hour", ascending=True)
                else:
                    raw_data_df = raw_data_df.sort_values(by="Visits", ascending=False)

                st.dataframe(raw_data_df)

        st.write("### AI Overview:")
        st.write(result)


    except Exception as e:
        st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
