import React, { useEffect, useState } from "react";
import { BASE_URL } from "../constants";
import axios from "axios";

const Book = (props) => {
  const [book, setBook] = useState("");
  const [characters, setCharacters] = useState("");

  const fetchBookByHandle = async (handle) => {
    const response = await axios.get(`${BASE_URL}/books/${handle}`);
    console.log("data", response.data);
  };

  useEffect(() => {
    fetchBookByHandle(props.handle);
  }, []);

  return (
    <div>
      <h1>Book {props.handle}</h1>
    </div>
  );
};

export default Book;
