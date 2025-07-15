import json

# Sample structure of geo_data data
data = {
  "Khyber Pakhtunkhwa": {
    "divisions": {
      "Malakand": ["Chitral", "Upper Dir", "Lower Dir", "Swat", "Shangla", "Buner", "Malakand", "Bajaur"],
      "Hazara": ["Kohistan", "Mansehra", "Batagram", "Abbottabad", "Haripur", "Torghar"],
      "Mardan": ["Mardan", "Swabi"],
      "Peshawar": ["Charsadda", "Peshawar", "Nowshera", "Khyber", "Mohmand"],
      "Kohat": ["Kohat", "Hangu", "Karak", "Kurram", "Orakzai"],
      "Bannu": ["Bannu", "Lakki Marwat", "North Waziristan"],
      "D.I. Khan": ["D.I. Khan", "Tank", "South Waziristan"]
    },
    "destinations": ["Khyber Pass", "Swat Valley", "Harnoi Abbottabad", "Kalash Valley", "Kaghan Valley"]
  },
  "Punjab": {
    "divisions": {
      "Rawalpindi": ["Attock", "Rawalpindi", "Jhelum", "Chakwal"],
      "Sargodha": ["Sargodha", "Bhakkar", "Khushab", "Mianwali"],
      "Faisalabad": ["Faisalabad", "Chiniot", "Jhang", "Toba Tek Singh"],
      "Gujranwala": ["Gujranwala", "Hafizabad", "Gujrat", "Mandi Bahauddin", "Sialkot", "Narowal"],
      "Lahore": ["Lahore", "Kasur", "Sheikhupura", "Nankana Sahib"],
      "Sahiwal": ["Okara", "Sahiwal", "Pakpattan"],
      "Multan": ["Vehari", "Multan", "Lodhran", "Khanewal"],
      "D.G. Khan": ["Dera Ghazi Khan", "Rajanpur", "Layyah", "Muzaffargarh"],
      "Bahawalpur": ["Bahawalpur", "Bahawalnagar", "Rahim Yar Khan"]
    },
    "destinations": ["Murree", "Narh Noorabad", "Badshahi Mosque", "Wagah border", "Khewra salt mine"]
  },
  "Sindh": {
    "divisions": {
      "Larkana": ["Jacobabad", "Kashmore", "Shikarpur", "Larkana", "Qambar Shahdadkot"],
      "Sukkur": ["Sukkur", "Ghotki", "Khairpur"],
      "Hyderabad": ["Dadu", "Jamshoro", "Hyderabad", "Tando Allahyar", "Tando Muhammad Khan", "Matiari", "Badin", "Thatta", "Sujawal"],
      "Mirpur Khas": ["Mirpur Khas", "Umerkot", "Tharparkar"],
      "Karachi": ["Karachi West", "Malir", "Karachi South", "Karachi East", "Karachi Central", "Korangi"],
      "Shaheed Benazirabad": ["Naushehro Feroze", "Shaheed Benazirabad", "Sanghar"]
    },
    "destinations": ["Mazar e Qaid", "Mohenjo-daro", "Lal Shahbaz Qalandar Shrine", "Keenjhar Lake", "Clifton Beach"]
  },
  "Balochistan": {
    "divisions": {
      "Quetta": ["Quetta", "Pishin", "Killa Abdullah"],
      "Zhob": ["Loralai", "Barkhan", "Musakhel", "Killa Saifullah", "Zhob", "Sherani", "Duki"],
      "Sibi": ["Sibi", "Harnai", "Ziarat", "Kohlu", "Dera Bugti"],
      "Nasirabad": ["Kachhi", "Jaffarabad", "Nasirabad", "Jhal Magsi", "Sohbatpur"],
      "Kalat": ["Kalat", "Mastung", "Khuzdar", "Awaran", "Lasbela", "Shaheed Sikandarabad"],
      "Makran": ["Kech", "Gwadar", "Panjgur"],
      "Rakhshan": ["Chagai", "Kharan", "Nushki", "Washuk"]
    },
    "destinations": ["Ziarat", "Gwadar", "Hingol National Park", "Turbat", "Ormara Beach"]
  },
  "Islamabad": {
    "divisions": {
      "Islamabad Division": ["Islamabad"]
    },
    "destinations": ["Shah Faisal Mosque", "Margalla Hills", "Daman-e-Koh", "Pakistan Monument", "Supreme court of Pakistan"]
  },
  "Gilgit-Baltistan": {
    "divisions": {
      "Gilgit": ["Gilgit", "Ghizer", "Hunza", "Nagar"],
      "Baltistan": ["Ghanche", "Shigar", "Kharmang"],
      "Astore": ["Diamir", "Astore"]
    },
    "destinations": ["Pak China Border", "Attabad Lake", "Hunza Valley", "Deosai National Park", "Altit Fort"]
  },
  "Azad Jammu and Kashmir": {
    "divisions": {
      "Muzaffarabad": ["Muzaffarabad", "Neelum", "Hattian Bala"],
      "Poonch": ["Bagh", "Sudhnoti", "Poonch", "Haveli"],
      "Mirpur": ["Bhimber", "Mirpur", "Kotli"]
    },
    "destinations": ["Neelum Valley", "Pir Chinasi", "Mangla Dam", "Ratti Gali Lake", "Gurez Valley"]
  }
}


modes = ["bus", "car", "air"]

fares_list = []

# Simple fare generator function
def generate_fare(source, destination, mode):
    base = 1000 + (len(source) * 10) + (len(destination) * 15)
    if mode == "bus":
        return base
    elif mode == "car":
        return base * 2
    else:  # air
        return base * 4

# Generate fares
for province_src, info_src in data.items():
    for division, districts in info_src["divisions"].items():
        for district in districts:
            for province_dst, info_dst in data.items():
                for destination in info_dst["destinations"]:
                    for mode in modes:
                        fare = generate_fare(district, destination, mode)
                        fares_list.append({
                            "source": district,
                            "destination": destination,
                            "mode": mode,
                            "fare": fare
                        })

# Save to JSON file
with open("fares.json", "w") as f:
    json.dump(fares_list, f, indent=4)

print("Fares JSON file created successfully.")
