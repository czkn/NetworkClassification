import subprocess, struct, time, select, threading, os, sys, traceback, itertools,math, collections
import pytcpdump
import re
import tldextract
import numpy as np
import math

#***********************************************************************************
# Header for csv with statistical features
#***********************************************************************************
def stat_head():
	return "sni,CSPktNum,CSPktsize25,CSPktSize50,CSPktSize75,CSPktSizeMax,CSPktSizeAvg,CSPktSizeVar,CSPaysize25,CSPaySize50,CSPaySize75,CSPaySizeMax,CSPaySizeAvg,CSPaySizeVar,CSiat25,CSiat50,CSiat75,SCPktNum,SCPktsize25,SCPktSize50,SCPktSize75,SCPktSizeMax,SCPktSizeAvg,SCPktSizeVar,SCPaysize25,SCPaySize50,SCPaySize75,SCPaySizeMax,SCPaySizeAvg,SCPaySizeVar,SCiat25,SCiat50,SCiat75,PktNum,Pktsize25,PktSize50,PktSize75,PktSizeMax,PktSizeAvg,PktSizeVar,iat25,iat50,iat75\n"

#***********************************************************************************
# Header for csv with sequence features
#***********************************************************************************
def sequence_head(n):
	return "sni," + ','.join([str(i) for i in range(1,n)]) + "\n"

#***********************************************************************************
# Get features for packets/payloads (25th, 50th, 75th) percentiles, max, mean, var
#***********************************************************************************
def stat_calc(x, iat=False):
	if len(x)==0:
		return [str(a) for a in [0,0,0,0,0,0]]
	if len(x)==1:
		return [str(a) for a in [x[0], x[0], x[0], x[0], x[0], 0]]
	x = sorted(x)
	p25,p50,p75 = get_percentiles(x)
	return [str(a) for a in [p25,p50,p75,max(x),np.mean(x),np.var(x)]]

#***********************************************************************************
# Helper function to get percentiles
#***********************************************************************************
def get_percentiles(x):
	return x[int(round((len(x)-1)/4.0))], x[int(round((len(x)-1)/2.0))], x[int(round((len(x)-1)*3/4.0))]

#***********************************************************************************
# Helper function to combine milliseconds/seconds timestamps
#***********************************************************************************
def combine_at(sec, usec):
	l = len(sec)
	return [sec[i]+usec[i]*1e-6 for i in range(l)]

#***********************************************************************************
# Get features for inter-arrival times (25th, 50th, 75th) percentiles
#***********************************************************************************
def stat_prepare_iat(t):
	l = len(t)
	iat = [t[i+1]-t[i] for i in range(l-1)]
	if len(iat)==0:
		return [str(a) for a in [0,0,0]]
	if len(iat)==1:
		return [str(a) for a in [iat[0], iat[0], iat[0]]]
	p25,p50,p75 = get_percentiles(iat)
	return [str(a) for a in [p25,p50,p75]]

#***********************************************************************************
# Get statistical features from tcp packet sequences
#***********************************************************************************
def stat_create(data,filename,first_n_packets):
	with open(filename,'w') as f:
		f.write(stat_head())
		for id in data:
			item=data[id]

			sni=SNIModificationbyone(item[0])

			# exclude unknown domains
			if sni == 'unknown' or sni == 'unknown.':
				continue

			line=[sni]

			# remote->local features
			# 1 length 
			# 2-7 packets stats			
			# 8-14 payload stats
			# 15-17 inter-arrival time stats
			line+=[str(len(item[4][0]))]
			line+=stat_calc(item[4][0])
			line+=stat_calc(item[5][0])
			arrival1=combine_at(item[2][0], item[3][0])
			line+=stat_prepare_iat(arrival1)
			
			# local->remote
			# 18 length 
			# 19-24 packets stats			
			# 25-30 payload stats
			# 31-33 inter-arrival time stats
			line+=[str(len(item[4][1]))]
			line+=stat_calc(item[4][1])
			line+=stat_calc(item[5][1])
			arrival2=combine_at(item[2][1], item[3][1])
			line+=stat_prepare_iat(arrival2)

			# both
			# 34-39 packets stats			
			# 40-42 inter-arrival time stats
			line+=[str(len(item[4][1]) + len(item[4][0]))]
			line+=stat_calc(item[4][1] + item[4][0])
			line+=stat_prepare_iat(sorted(arrival1 + arrival2))

			line= ','.join(line)
			f.write(line)
			f.write('\n')

#***********************************************************************************
# Create features from tcp packet sequences
#***********************************************************************************
def sequence_create(data, filename, first_n_packets):
	with open(filename,'w') as f:
		f.write(sequence_head(first_n_packets))
		counter = 0
		skipped = 0
		for id in data:
			item=data[id]
			sni=SNIModificationbyone(item[0])

			# exclude unknown domains
			counter = counter + 1
			if sni == 'unknown' or sni == 'unknown.':
				skipped = skipped + 1
				continue

			line=[sni]

			# Calculate arrival times in millis for local->remote and remote->local
			arrival1=combine_at(item[2][0], item[3][0])
			arrival2=combine_at(item[2][1], item[3][1])
			
			# Sort all packets by arrival times to get sequence in correct order
			packets = zip(arrival1 + arrival2, list(item[4][0]) + list(item[4][1]))
			packets = [str(x) for _,x in sorted(packets)]

			# Zero padding for sequences that are too short
			if len(packets) < first_n_packets:
				packets = [str(0)]*(first_n_packets - len(packets)) + packets

			line+=packets[0:first_n_packets]

			# Sort all payloads by arrival times to get sequence in correct order
			payloads = zip(arrival1 + arrival2, list(item[5][0]) + list(item[5][1]))
			payloads = [str(x) for _,x in sorted(payloads)]

			# Zero padding for sequences that are too short
			if len(payloads) < first_n_packets:
				payloads = [str(0)]*(first_n_packets - len(payloads)) + payloads

			line+=payloads[0:first_n_packets]

			# Sort all packets by arrival times to get sequence in correct order
			arrivals = sorted(arrival1 + arrival2)
			iat = [str(0)] + [str(arrivals[i+1]-arrivals[i]) for i in range(len(arrivals)-1)]

			# Zero padding for sequences that are too short
			if len(iat) < first_n_packets:
				iat = [str(0)]*(first_n_packets - len(iat)) + iat

			line+=iat[0:first_n_packets]

			# Sort all directions by arrival times to get direction sequence in correct order (-1, 1, 0)
			# remote -> local = -1
			# local -> remote = 1
			# padding = 0
			direction = zip(arrival1 + arrival2, [-1]*len(item[5][0]) + [1]*len(item[5][1]))
			direction = [str(x) for _,x in sorted(direction)]

			# Zero padding for direction sequences that are too short
			if len(direction) < first_n_packets:
				direction = [str(0)]*(first_n_packets - len(direction)) + direction

			line+=direction[0:first_n_packets]

			line= ','.join(line)
			f.write(line)
			f.write('\n')
		print("Skipped percentage: ", 1. * skipped / counter)

#***********************************************************************************
# Parts of this function borrowed from the following paper:
#
# Multi-Level identification Framework to Identify HTTPS Services
# Author by Wazen Shbair,
# University of Lorraine,
# France
# wazen.shbair@gmail.com
# January, 2017
#
# SNi modification for the sub-domain parts only
#***********************************************************************************
def SNIModificationbyone(sni):
    temp = tldextract.extract(sni.encode().decode())
    x = re.sub("\d+", "", temp.subdomain)  # remove numbers
    x = re.sub("[-,.]", "", x)  #remove dashes
    x = re.sub("[(?:www.)]", "", x) #remove www
    if len(x) > 0:
        newsni = x + "." + temp.domain + "." + temp.suffix  # reconstruct the sni
    else:
        newsni = temp.domain + "." + temp.suffix

    return newsni

#***********************************************************************************
# Inputs
# 1. pcap file (filtered for SSL)
# 2. output file for statistical features
# 3. output file for sequence features
#***********************************************************************************
if __name__ == "__main__":
	pcap_file = ['../pcaps/GCDay1SSL.pcap', '../pcaps/GCDay2SSL.pcap','../pcaps/GCDay3SSL.pcap',
	'../pcaps/GCDay4SSL.pcap','../pcaps/GCDay5SSL.pcap','../pcaps/GCDay6SSL.pcap',
	'../pcaps/GCDay7SSL.pcap','../pcaps/GCDay8SSL.pcap','../pcaps/GCDay9SSL.pcap',
	'../pcaps/GCDay10SSL.pcap','../pcaps/GCDay11SSL.pcap','../pcaps/GCDay12SSL.pcap']
	output_file_stats = '../ML/training/GCstats.csv'
	output_file_seqs = '../DL/training/GCseq25.csv'
	for fname in pcap_file:
		print ('process', fname)
		pytcpdump.process_file(fname)
		print (fname,"finished, kept",len(pytcpdump.cache.cache),'records')

	stat_create(pytcpdump.cache.cache, output_file_stats, first_n_packets=25)
	sequence_create(pytcpdump.cache.cache, output_file_seqs, first_n_packets=25)
