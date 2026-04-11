from fastapi import HTTPException, APIRouter
from app.db.database import get_db_connection
from psycopg2.extras import RealDictCursor
from typing import List
from app.models.model import UserCreate, UserResponse, FoodListingCreate, FoodListingResponse

router=APIRouter()

# This method creates a new user in the database
@router.post("/users", response_model=UserResponse) #Gets the input and validates
def create_user(user: UserCreate):
    conn=get_db_connection() # Establishes a connection with the database
    if not conn:
        raise HTTPException(status_code=500, detail="Database Connection Failed!!!")
    try:
        cursor=conn.cursor(cursor_factory=RealDictCursor) # Alert the database query editor
        query="""  
            INSERT INTO users (name, role, email)
            VALUES (%s, %s, %s) RETURNING *;
        """
        # Main query for posting new user in db
        cursor.execute(query, (user.name, user.role, user.email)) # Performs the query operation
        new_user=cursor.fetchone() # Gets the newly added user details
        conn.commit() # Finishes the execution
        return new_user
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close() # Closes the connection with database

# This method creates a new food item in the database
@router.post("/food", response_model=FoodListingResponse)
def create_food_listing(food: FoodListingCreate):
    conn=get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database Connection Failed!!!")
    try:
        cursor=conn.cursor(cursor_factory=RealDictCursor)
        query="""
            INSERT INTO food_listings (title, description, qty, provider_id)
            VALUES (%s,%s,%s,%s) RETURNING *;
        """
        cursor.execute(query, (food.title, food.description, food.qty, food.provider_id))
        new_food=cursor.fetchone()
        conn.commit()
        return new_food
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

@router.get("/food",response_model=List[FoodListingResponse])
def get_food_listing():
    conn=get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database Connection Failed!!!")
    try:
        cursor=conn.cursor(cursor_factory=RealDictCursor)
        query="""
            SELECT * FROM food_listings 
            WHERE status='available';
        """
        cursor.execute(query)
        foods=cursor.fetchall()
        conn.commit()
        return foods
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()


@router.post("/food/{food_id}/claim", response_model=FoodListingResponse)
def claim_food(food_id: int, claimed_id: int):
    conn=get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database Connection Failed!!!")
    try:
        cursor=conn.cursor(cursor_factory=RealDictCursor)
        query="""
            UPDATE food_listings
            SET claimed_id=%s, status='claimed'
            WHERE status='available' AND id=%s
            RETURNING *;
        """
        cursor.execute(query, (claimed_id, food_id))
        updated_food=cursor.fetchone()
        conn.commit()
        if not updated_food:
            raise HTTPException(status_code=404, detail="No Such Food (or) Already Claimed")
        return updated_food
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()




