
**You are a senior full-stack AI engineer and system architect.
Your task is to design and build an end-to-end prototype project called *“Threads of Tradition”*.
This project is a functional demo (not a production-ready app) that demonstrates frontend, backend, AI features, and data flow clearly.**

---

## 🔹 1. Project Overview

**Project Name:** Threads of Tradition

**Problem Statement:**
Traditional Indian handloom and handmade artisans are becoming endangered due to dominance of foreign e-commerce platforms. Customers cannot easily find authentic handloom products or verify whether items are genuinely made by Indian artisans. Additionally, many rural artisans lack digital marketing knowledge and struggle with pricing their work fairly.

**Solution:**
Threads of Tradition is a platform with:

* An **Artisan Portal** for verified artisans to showcase their handmade work
* A **Shopping Portal** for users to view and browse these products
* AI-powered assistance for **caption generation** and **price recommendation**

---

## 🔹 2. System Architecture (High Level)

Build the system with:

* **Frontend** (Artisan Portal + Shopping Portal)
* **Backend APIs**
* **AI services (NLP-based caption generator & rule/ML-based price estimator)**
* **Database**
* **Fake/demo verification & certificates (mocked, not real)**

The project should work end-to-end as a **demonstration prototype**.

---

## 🔹 3. User Roles

### 👩‍🎨 Artisan

* Registers and logs in
* Uploads handmade product images
* Enters:

  * Time spent making the product
  * Material used
* Gets:

  * Auto-generated product caption
  * Recommended price range
* Products appear on shopping portal

### 🛍️ Customer (Shopping Portal User)

* Views listed products
* Sees:

  * Product image
  * AI-generated caption
  * Recommended price
  * “Verified Artisan” badge
  * Fake/generated certificate label

### 🛠️ Admin (Optional / Simple)

* Can view artisan registrations
* Marks artisans as “Verified” (manual toggle / mock verification)

---

## 🔹 4. Artisan Portal – Functional Requirements

1. **Artisan Registration Page**

   * Name
   * Location
   * Artisan ID / Certificate upload (mock verification)
   * Login credentials

2. **Product Upload Page**

   * Upload image of handmade product
   * Enter:

     * Time taken (hours/days)
     * Material used (cotton, silk, wool, etc.)

3. **AI Features**

   * **Caption Generator**

     * Automatically generates a selling caption when image is uploaded
     * Caption should highlight:

       * Tradition
       * Handcrafted nature
       * Material
       * Cultural value
   * **Price Recommendation**

     * Suggests a reasonable price range based on:

       * Time spent
       * Material type
       * Handmade factor
     * Logic can be rule-based or ML-inspired (no need for real model training)

4. **Preview**

   * Artisan sees final product preview before submission

---

## 🔹 5. Shopping Portal – Functional Requirements

* Display products submitted by artisans

* Each product card should show:

  * Product image
  * Generated caption
  * Recommended price range
  * Artisan name & location
  * “Verified Artisan” badge
  * Fake/generated certificate ID (demo purpose only)

* Include:

  * Simple grid layout
  * Filters (optional): material, price range

⚠️ No real payment gateway required — display-only portal.

---

## 🔹 6. AI / ML Components

### 🔹 Caption Generation

* Use NLP-based text generation (template + AI logic)
* Input:

  * Product image (optional reference)
  * Material
  * Handmade context
* Output:

  * Marketing-style caption

### 🔹 Price Recommendation

* Input:

  * Time spent
  * Material type
* Output:

  * Suggested price range
* Can use:

  * Rule-based logic (preferred for demo)
  * Example:

    * More time + premium material → higher price

---

## 🔹 7. Tech Stack (Suggested – you may choose similar)

### Frontend:

* HTML, CSS, JavaScript
* OR React (preferred if possible)

### Backend:

* Python with Flask (preferred)
* REST APIs

### Database:

* SQLite / MySQL (simple schema)

### AI / Logic:

* Python NLP (basic text generation)
* Rule-based price logic

---

## 🔹 8. Data Flow

1. Artisan registers → stored in database
2. Artisan uploads product → backend processes input
3. Caption generator runs → caption saved
4. Price recommendation runs → price saved
5. Product appears on shopping portal automatically

---

## 🔹 9. Deliverables Expected from You (Agent)

1. **Frontend**

   * Artisan portal UI
   * Shopping portal UI

2. **Backend**

   * APIs for:

     * Registration
     * Product upload
     * Caption generation
     * Price recommendation
     * Product listing

3. **Database Schema**

   * Artisan table
   * Product table

4. **AI Logic**

   * Caption generator logic
   * Price recommendation logic

5. **Fake Verification System**

   * Dummy artisan verification
   * Auto-generated fake certificate ID

6. **Documentation**

   * Project explanation
   * Architecture
   * How to run locally

---

## 🔹 10. Important Constraints

* This is a **prototype / academic project**
* No real payments
* No real certificate validation
* Focus on **working demo + social impact**

---

## 🔹 11. Final Goal

Deliver a **fully connected demo system** that clearly demonstrates:

* Artisan empowerment
* AI assistance for rural artisans
* Preservation of Indian handloom tradition
* End-to-end full-stack + AI integration
