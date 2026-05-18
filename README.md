# Aurum - Luxury E-Commerce Platform

A SaaS luxury e-commerce platform built with FastAPI and Vanilla JS/HTML/CSS.

## Features
- Complete shopping flow: product browsing, cart, and checkout.
- Persistent database-backed cart.
- Secure, protected Admin Dashboard.
- Clean, luxury aesthetic with custom UI components.
- Secure by default (rate limiting, secure headers, CORS, etc.).

## User & Admin Roles
- **Default Users**: Can browse the shop, view products, manage their cart, and place orders.
- **Admin Users**: Have access to the Admin Dashboard to manage products and fulfill orders.

### Managing Products
As an admin, you can:
1. **Add Products**: Fill out the "Add New Product" form on the dashboard to instantly make a product available on the shop.
2. **Delete Products**: Below the add form is the "Manage Products" table. Click the **Delete** button next to any product to remove it from the store permanently.

### Order Fulfillment (Shipping)
1. When users check out, their orders appear in the **Manage Orders** table on the Admin Dashboard with a `PENDING` status.
2. To ship an order, click the **Ship** button. 
3. The order status updates to `DELIVERED`, which immediately reflects on the user's personal dashboard as well!

## Installation
1. `pip install -r requirements.txt`
2. Copy `.env.example` to `.env` and fill in your secrets.

## How to Run
```bash
uvicorn BackEnd.main:app --reload
```
Then navigate to `http://localhost:8000` in your browser.

## Environment Variables
See `.env.example` for details.
