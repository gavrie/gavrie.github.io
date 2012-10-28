---
layout: post
title: "Generating Virtual FC WWPNs for a Storage Lab"
date: 2012-02-16 16:30
comments: true
categories: [storage, fibre channel]
published: true
---

At work, I encountered an interesting problem: While testing the Fibre Channel (FC)
scalability of a storage product, we needed to create a *lot* of FC connections between hosts and the storage system. This would in turn require a large number of FC Initiators, each of which having a unique [World-Wide Port Name (WWPN)](http://en.wikipedia.org/wiki/World_Wide_Port_Name).

The easiest and cheapest method to set up a lot of initiators without actually purchasing zillions of FC HBAs would be to use [N_Port ID Virtualization](http://en.wikipedia.org/wiki/NPIV), a.k.a. NPIV. This method allows a single FC HBA to present itself to the FC fabric with multiple WWPNs. This, in turn, allows the creation of many connections to the target storage device from a small number of hosts.


The Problem
-----------

WWPNs can't just be pulled out of thin air. They are allocated -- in chunks -- by a central authority, the [IEEE Registration Authority](http://standards.ieee.org/develop/regauth/). Just making up random WWPNs could cause trouble for two reasons:

1. The WWPN must be unique on the fabric, which means it must be generated in a deterministic way so that two hosts won't be using the same WWPN and thereby confuse the fabric.
2. The WWPN should not have a chance of clashing with official WWPNs of purchased HBAs.

With physical (as opposed to virtual) HBAs, this is managed by allocating a OUI (Organizationally Unique Identifier) to every vendor, who in turns tacks on his own vendor-specific serial number to come up with a unique WWPN. This is similar to the MAC address allocation of Ethernet, Wi-Fi and Bluetooth devices.

The textbook solution for our problem would have involved the use of an officially allocated OUI to generate legal WWPNs, but that seemed like overkill for lab project which would never be used on a production SAN.

<!-- more -->

Some Background
---------------

We now require a kind of a compromise which takes care of the above two issues without causing too much bureaucratic pain. To reach such a solution, we'll refer to the IEEE's [Guidelines for Fibre Channel Use of the Organizationally Unique Identifier (OUI)](http://standards.ieee.org/develop/regauth/tut/fibre.pdf), and cheat a bit.

Let's assume that we have an FC HBA with a WWPN of `10:00:00:00:c9:93:53:6d`.
We'll decode it according to the IEEE Guidelines:

    10:00:vv:vv:vv:ss:ss:ss
    \___/ \______/ \______/
      |      |        |
      |      |        |
      |      |         \__ Vendor-specific part (24 bits)
      |      |
      |       \__ Vendor OUI (24 bits)
      |
       \__ This WWPN uses the Original WWN format


According to this diagram, our sample WWPN contains the following information:

* The `10:00` prefix means that it uses the original WWN format (a.k.a. "NAA IEEE 48-bit address format"), as opposed to newer formats that starting with another sequence
* The vendor is `00:00:c9`, which is an OUI belonging to Emulex Corporation 
  (according to the [OUI list](http://standards.ieee.org/develop/regauth/oui/oui.txt))
* The vendor-specific part is `93:53:6d`, which is 24 bits long


Using One WWPN to Generate Many New Ones
----------------------------------------

For every physical WWPN, we need to be able to generate up to 256 virtual WWPNs to be used with NPIV (assuming that each HBA port supports up to 256 virtual ports). The trick lies in reusing the vendor-specific part to generate multiple WWPNs per physical port, each of which would be guaranteed to be unique throughout the lab.

For that, we rely on the existence of a newer WWN format ("NAA IEEE Registered") that has more space for the vendor-specific part:


    5v:vv:vv:vs:ss:ss:ss:ss
    |\_______/\___________/
    |   |        |
    |   |        |
    |   |         \__ Vendor-specific part (extended to 36 bits)
    |   |
    |    \__ Vendor OUI (still 24 bits)
    |
     \__ Newer WWN format (NAA IEEE Registered)


Good, we now have 36 bits for the vendor-specific part!

We will use the larger vendor-specific field to include *both* the vendor-specific part of the physical ports WWPN (which is just 24 bits), *and* our own 12-bit custom part. This will let us generate up to 2<sup>12</sup> = 4096 virtual ports per physical port, which is more than enough.

Just to be safe, and to avoid a future clash with HBAs from the same vendor who might use the new numbering scheme as well, we'll modify the OUI to a currently unused one (`0000c8` instead of `0000c9`). This is of course not 100% future-proof, but is good enough for our purposes.

This leads us to the following range of generated WWPNs:

    Original WWPN:

        10:00:00:00:c9:93:53:6d, semantically represented as:

        1000 0000c9 93536d
             \____/ \____/
               |      |
             vendor   |
                    serial

    Generated WWPN range:

        5 0000c8 93536d 000
        5 0000c8 93536d 001
        5 0000c8 93536d 002
        ...
        5 0000c8 93536d fff
          \____/ \____/ \_/
            |      |     |
          vendor   |    custom
                 serial


Conclusion
----------

While still being a hack, the above scheme allows us to generate as many WWPNs as we need.

It has the advantage of being intuitive, since it is easy to determine just by looking at the WWPNs which ones of them are physical (starting with `1000 0000c9`) and which are virtual (starting with `5 0000c8`).

It also makes it easy to see which virtual WWPNs belong to each physical port, which is important for debugging purposes: The serial number of the physical port (`93536d`) is part of the virtual port's WWPN as well.
