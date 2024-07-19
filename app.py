import streamlit as st
import xml.etree.ElementTree as ET

def extract_podcast_info(xml_string):
    xml_string = xml_string.lstrip()
    start_index = xml_string.find('<?xml')
    if start_index != -1:
        xml_string = xml_string[start_index:]
    else:
        st.warning("XML declaration not found. This might cause issues.")
    
    try:
        root = ET.fromstring(xml_string)
    except ET.ParseError as e:
        st.error(f"Error parsing XML: {e}")
        return None
    
    items = root.findall(".//item")
    st.info(f"Found {len(items)} item elements in the XML")
    
    podcast_info = []
    for item in items:
        title_elem = item.find("title")
        title = title_elem.text if title_elem is not None else "No title"
        
        enclosure = item.find("enclosure")
        if enclosure is not None:
            mp3_url = enclosure.get('url')
            if mp3_url and '.mp3' in mp3_url:
                mp3_url = mp3_url.split('.mp3')[0] + '.mp3'  # Remove everything after .mp3
                podcast_info.append({
                    "title": title,
                    "mp3_url": mp3_url
                })
    
    return podcast_info

st.title('Podcast MP3 Link Extractor')

xml_input = st.text_area("Paste your XML here:", height=300)

if xml_input:
    st.write("Processing XML input...")
    podcast_info = extract_podcast_info(xml_input)
    if podcast_info is not None:
        if podcast_info:
            st.success(f"Found {len(podcast_info)} podcast episode(s) with MP3 links:")
            for info in podcast_info:
                st.write(f"Title: {info['title']}")
                st.write(f"MP3 URL: {info['mp3_url']}")
                
                # Create a download link
                st.markdown(f"[Download {info['title'][:30]}...]({info['mp3_url']})")
                
                st.write("---")
        else:
            st.warning("No podcast episodes with MP3 links found in the provided XML.")
    st.write("XML processing complete.")
else:
    st.info("Please paste XML content to extract podcast information and MP3 links.")
