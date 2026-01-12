# **FrescoCluster** 🎨
**Advanced Image Clustering Tool for Fresco Analysis**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.9.0-green)](https://opencv.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4.2-orange)](https://scikit-learn.org/)

---

## 📌 **About the Project**
**FrescoCluster** is an advanced desktop application designed for digital analysis and clustering of fresco images using the **K-means algorithm** with grid optimization. Developed for art historians, restorers, and digital humanities researchers, this tool enables precise color structure analysis of frescoes.

### **Key Features**
✔ **Grid-Based Clustering** – Apply K-means with adjustable grid steps for precise analysis
✔ **Real-Time Preview** – Instant visualization of clustering results with opacity control
✔ **Performance Optimized** – Uses **MiniBatch K-means** for fast processing of large images
✔ **User-Friendly UI** – Modern interface built with **CustomTkinter**
✔ **Benchmarking Support** – Includes tools for performance measurement and optimization

---

## 🚀 **Installation**

### **Prerequisites**
- Python **3.10+**
- OS: **Windows/Linux/macOS**

### **Installation Steps**
1. Clone the repository:
   ```
   bash
   git clone https://github.com/yourusername/FrescoCluster.git
   cd FrescoCluster
   ```



2. Install dependencies:
    ```
    bash
    pip install -r requirements.txt
    ```


3. Run the application:
    ```
    bash
    python app.py
    ```

---

## 🛠 User Guide
1. Loading an Image
   
    - Click "Upload Image" to select a fresco image (JPEG/PNG).
    - The system automatically resizes large images for optimal performance.
2. Adjusting Parameters
   
    - Number of Clusters (K): Controls color segmentation precision (3-8 recommended).
    - Grid Step: Defines the block size for grid-based processing (5-20 pixels recommended).
3. Applying Clustering
   
    - Click "Apply Clustering" to process the image.
    - Use the opacity slider to compare the original and clustered versions.
4. Saving Results
    - Click "Save Clustered Image" to export the processed image.

---

## 📊 Benchmarking Results

|Image Size|300×300 pixels|800×800 pixels|2000×2000 pixels|
-----------|--------------|--------------|----------------|
|K=3|0.017s|0.052s|0.275s|
|K=5|0.022s|0.077s|0.334s|
|K=8|0.030s|0.174s|1.059s|

### Optimal Settings:

K=5, Grid Step=10 – Best balance of speed and quality.

Avoid K=8 + Grid Step=10 for large images (slowest combination).

---

## 🔧 Development & Customization
### Extending Functionality

- GPU Acceleration: Integrate with CuPy for faster computations.
- Additional Algorithms: Implement DBSCAN or MeanShift for comparison.
- Auto-Parameter Selection: Optimize settings based on image size.

---

### Contributing

Fork the repository.
Create a feature branch:
```
git checkout -b feature/your-feature
```

Commit your changes:
```
git commit -m "Add your feature"
```

Push to the branch:
```
git push origin feature/your-feature
```

Open a Pull Request.

---

###📜 License
This project is licensed under the MIT License – see LICENSE for details.

---

###🙌 Acknowledgments

- OpenCV & scikit-learn for image processing capabilities
- CustomTkinter for modern UI components
- Denys Kurishchenko for project concept and implementation

© 2026 FrescoCluster | Digital Art Analysis Tools
