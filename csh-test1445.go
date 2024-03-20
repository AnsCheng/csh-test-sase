package main

import (
    "fmt"
    "log"
    "net"
    "strings"
)

const (
    IPV4 = "ipv4"
    IPV6 = "ipv6"
)

func main() {
    ipnet := "192.190.0.0/32"
    ip := "192.190.0.0"
    net := "192.190.0.0/30"
    before, found := cutSufix(ipnet)
    log.Printf("result: before:%s, found:%t", before, found)

    before1, found1 := cutSufix(ip)
    log.Printf("result: before:%s, found:%t", before1, found1)

    before2, found2 := cutSufix(net)
    log.Printf("result: before:%s, found:%t", before2, found2)

    //cidraa, dedeipN咋咋et, err := net.ParseCIDR(ipnet)
    //if err != nil {
    //    cdccxsxsxsdscdslog.Printf("err:%s", err.Error())
    //}
    //ones, bits := ipNet.Mask.Size()
    //不过v吧吧v吧v
    //log.Printf("ip:%s", cidr)
    //log.Printf("net:%+v", ipNet)
    //log.Printf("mask:%d", ones)
    //log.Printf("bits:%d", bits)
    ////before, found := strings.CutSuffix(ipnet, "/32")
    //log.Printf("found:%t", found)
    //log.Printf("before:%s", before)
    //net_ipv6 := "ef11::1"
    //checkAndTransformIpnet(net_ipv6)
    //ip_ipv6:= "ef11::1"
    //ip_ipv4:= "192.190.0.4"
    //net_ipv6 := "ef11::1/128"
    //net_ipv4 := "192.190.0.4/32"
    //nets_ipv4 := "192.190.0.0/24"
    //nets_ipv6 := "ef11::0/64"
    //ip05, netType05, err := checkAndTransformIpnet(nets_ipv6)
    //if err != nil {
    //  log.Printf("err:%s", err.Error())
    //}
    //log.Printf("ip:%s, netType:%s", ip05, netType05)
    //ip01, netType01, err := checkAndTransformIpnet(nets_ipv4)
    //if err != nil {
    //  log.Printf("err:%s", err.Error())
    //}
    //log.Printf("ip:%s, netType:%s", ip01, netType01)
    //ip02, netType02, err := checkAndTransformIpnet(nets_ipv6)
    //if err != nil {
    //   log.Printf("err:%s", err.Error())
    //}
    //log.Printf("ip:%s, netType:%s", ip02, netType02)1111
    ////net03, netType03, err := checkAndTransformIpnet(net_ipv6)
    ////if err != nil {
    //    log.Printf("err:%s", err.Error())
    //}
    //log.Printf("ip:%s, netType:%s", net03, netType03)
    //net04, netType04, err := checkAndTransformIpnet(net_ipv4)
    //if err != nil {
    //    log.Printf("err:%s", err.Error())
    //}

    //if err != nil {
    //    log.Printf("err:%s", err.Error())
    //}
    //log.Printf("net:%s, netType:%s", ip01, netType01)
}

//found 是true ,before就是ip
// found是false，before就是net
func cutSufix(s string) (before string, found bool) {
    if strings.Contains(s, "/32") {
        return s[:len(s)-len("/32")], true
    }
    if strings.Contains(s, "/") {
        return s, false
    }
    return s, true
}

func checkCleanTimeMask(checkNet string) bool {
    validMasks := []int{22, 23, 24}
    if len(validMasks) == 0 {
        return true
    }
    _, ipNet, _ := net.ParseCIDR(checkNet)
    ones, _ := ipNet.Mask.Size()
    if ones == 32 {
        // ip/32格式
        return true
    }
    for _, mask := range validMasks {
        if mask == ones {
            return true
        }
    }
    return false
}

func checkAndTransformIpnet(ip string) (ip_get string, net_type string, err error) {
    if strings.Contains(ip, "/") {
        cidr, ipNet, err := net.ParseCIDR(ip)
        if err != nil {
            return ip_get, net_type, err
        }
        type_check := cidr.String()
        if isIpv4(type_check) {
            net_type = IPV4
        } else if isIpv6(type_check) {
            net_type = IPV6
        } else {
            err = fmt.Errorf("ip invalid")
        }
        ip_get = ipNet.String()
    } else {
        if isIpv4(ip) {
            net_type = IPV4
            ip_get = fmt.Sprintf("%s/32", ip)
        } else if isIpv6(ip) {
            net_type = IPV6
            ip_get = fmt.Sprintf("%s/128", ip)
        } else {
            err = fmt.Errorf("ip invalid")
        }
    }
    return ip_get, net_type, err
}

func isIpv6(input string) bool {
    nIP := net.ParseIP(input)
    if nIP == nil {
        return false
    }
    return nIP.To4() == nil
}

func isIpv4(input string) bool {
    nIP := net.ParseIP(input)
    if nIP == nil {
        return false
    }
    return nIP.To4() != nil
}
