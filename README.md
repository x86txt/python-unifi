# 🚀 UniFi Python CI/CD

A **personal project** to programmatically add dynamic lists (like source IP lists) to a **UniFi** controller.  
This enables **policy-based routing** for services like **Microsoft Teams Video**, ensuring it always uses the best **multi-WAN connection**.

---

## 🛠️ Installation & Usage

1. Clone the repository:

   ```sh
   git clone https://github.com/x86txt/python-unifi.git
   cd python-unifi
   ```

2. Modify `config.py` with your values.

3. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. Run the module:
   ```sh
   python -m unifi
   ```

---

## ❤️ Huge Thanks

This project **wouldn’t be possible** without the amazing work by:  
[Kane610/aiounifi](https://github.com/Kane610/aiounifi) ❤️

---

## 📝 License

This project is **open-source** under the Unlicense License. See [LICENSE](LICENSE) for details.

---

## ⭐ Support & Contributions

If you find this useful, **give it a star ⭐** or feel free to contribute! Pull requests are welcome. 🚀

---

## 🔧 Future Enhancements

- ✅ Auto-detection of best WAN connection
- ✅ Enhanced logging & reporting
- ✅ Support for additional routing policies
