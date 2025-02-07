import React from 'react';
import { motion } from 'framer-motion';
import Image from 'next/image';

const ChatBubble = ({ message, isLoading }) => {
  if (!message) return null; 

  const bubbleStyle = {
    maxWidth: '300px',
    padding: '10px',
    backgroundColor: isLoading ? '#E0E0E0' : '#DCF8C6',
    borderRadius: '15px',
    position: 'relative',
    display: 'inline-block',
    textAlign: 'center',
  };

  const buyNowHandler = () => {
    alert(`Redirecting to buy: ${message.title}`);
  };

  return (
    <motion.div
      initial={{ scale: 0.8, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ type: "spring", stiffness: 100, damping: 10 }}
      style={bubbleStyle}
    >
      {typeof message === 'string' ? (
        <p>{message}</p>
      ) : (
        <div style={{  alignItems: 'start', textAlign: 'left' }}>
          <Image 
            src={message.thumbnail} 
            alt={message.title} 
            width={100}
            height={100}
            style={{ width: '100%', borderRadius: '10px', marginBottom: '5px' }} 
          />
          <h3 style={{ fontSize: '16px', fontWeight: 'bold', marginTop: '5px' }}>{message.title}</h3>
          
          <p 
            style={{
              fontSize: '12px',
              color: '#555',
              display: '-webkit-box',
              WebkitBoxOrient: 'vertical',
              WebkitLineClamp: 2,
              overflow: 'hidden',
            }}
          >
            {message.description}
          </p>

          <p style={{ fontSize: '14px', fontWeight: 'bold', margin: '5px 0' }}>${message.price}</p>
          <p style={{ fontSize: '12px', color: '#777' }}>⭐ {message.rating}</p>
          
          <button 
            onClick={buyNowHandler}
            style={{
              marginTop: '8px',
              padding: '5px 10px',
              fontSize: '12px',
              fontWeight: 'bold',
              backgroundColor: '#ff5722',
              color: '#fff',
              border: 'none',
              borderRadius: '5px',
              cursor: 'pointer',
            }}
          >
            Buy Now
          </button>
        </div>
      )}
    </motion.div>
  );
};

export default ChatBubble;
