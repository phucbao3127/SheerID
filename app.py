import streamlit as st
import subprocess
import sys
import os
import glob

st.set_page_config(page_title="Spotify SheerID Tool", page_icon="🎵")
st.title("🎵 Spotify Verification Tool")

# Form nhập liệu
with st.form("verify_form"):
    target_url = st.text_input("URL Xác minh:", placeholder="https://sheerid.com/...")
    use_proxy = st.checkbox("Sử dụng Proxy (Bắt buộc trên Streamlit Cloud)", value=True)
    proxy_str = st.text_input("Proxy (User:Pass@IP:Port):")
    submitted = st.form_submit_button("🚀 Chạy ngay")

if submitted:
    if not target_url:
        st.error("Thiếu URL!")
    else:
        st.info("Đang xử lý... (Sẽ mất khoảng 10-30 giây)")
        
        # Xây dựng câu lệnh
        cmd = [sys.executable, "main.py", target_url]
        if use_proxy and proxy_str:
            cmd.extend(["--proxy", proxy_str])
            
        try:
            # Chạy tool
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Hiển thị log
            with st.expander("Xem chi tiết Log (Click để mở)"):
                st.code(result.stdout)
                if result.stderr:
                    st.error(result.stderr)
            
            # Tìm và hiển thị ảnh kết quả (nếu tool tạo ra ảnh PNG/JPG)
            list_of_files = glob.glob('*.png') + glob.glob('*.jpg') 
            if list_of_files:
                latest_file = max(list_of_files, key=os.path.getctime)
                st.success(f"Đã tạo ảnh: {latest_file}")
                st.image(latest_file)
                
                # Nút tải về
                with open(latest_file, "rb") as file:
                    btn = st.download_button(
                        label="Tải ảnh về",
                        data=file,
                        file_name=latest_file,
                        mime="image/png"
                    )
            else:
                st.warning("Tool đã chạy xong nhưng không tìm thấy ảnh kết quả. Hãy kiểm tra Log.")
                
        except Exception as e:
            st.error(f"Lỗi: {e}")
