import sys
from time import time
HEADER_SIZE = 12

class RtpPacket:	
	header = bytearray(HEADER_SIZE)
	
	def __init__(self):
		pass
		
	def encode(self, version, padding, extension, cc, seqnum, marker, pt, ssrc, payload):
		"""Encode the RTP packet with header fields and payload."""
		timestamp = int(time())
		header = bytearray(HEADER_SIZE)
		# Fill the header bytearray with RTP header fields
		
		header[0] = (header[0] | version << 6) & 0xC0; #holds 2 bits
		header[0] = (header[0] | padding <<5); #holds 1 bit
		header[0] = (header[0] | extension <<4); #holds 1 bit
		header[0] = (header[0] | (cc & 0x0F)); #holds 4 bits
		header[1] = (header [1] | marker <<7); #holds 1 bit
		header[1] = (header [1] | (pt & 0x7F)); #holds 7 bits
		header[2] = (seqnum & 0xFF00) >> 8; #holds 8 bits
		header[3] = (seqnum & 0xFF); #holds 8 bits
		#This holds a 32 bit timestamp of the packet
		header[4] = (timestamp >> 24); #first 8 bits
		header[5] = (timestamp >> 16) & 0xFF; #second 8 bits
		header[6] = (timestamp >> 8) & 0xFF; #third 8 bits
		header[7] = (timestamp & 0xFF); #fourth and final 8 bits
		#This holds our 32 bit SSRC
		#The SSRC is used for the cases of the RTP which chooses
		#a random value and identifies the synchronization source
		header[8] = (ssrc >> 24);
		header[9] = (ssrc >> 16) & 0xFF;
		header[10] = (ssrc >> 8) & 0xFF;
		header[11] = ssrc & 0xFF;
		
		#Above we created the bytearray for the RTP this packets our array
		#into our header on the packet
		self.header = header
		# Get the payload from the argument
		self.payload = payload
		
	def decode(self, byteStream):
		"""Decode the RTP packet."""
		self.header = bytearray(byteStream[:HEADER_SIZE])
		self.payload = byteStream[HEADER_SIZE:]
	
	def version(self):
		"""Return RTP version."""
		return int(self.header[0] >> 6)
	
	def seqNum(self):
		"""Return sequence (frame) number."""
		seqNum = self.header[2] << 8 | self.header[3]
		return int(seqNum)
	
	def timestamp(self):
		"""Return timestamp."""
		timestamp = self.header[4] << 24 | self.header[5] << 16 | self.header[6] << 8 | self.header[7]
		return int(timestamp)
	
	def payloadType(self):
		"""Return payload type."""
		pt = self.header[1] & 127
		return int(pt)
	
	def getPayload(self):
		"""Return payload."""
		return self.payload
		
	def getPacket(self):
		"""Return RTP packet."""
		return self.header + self.payload