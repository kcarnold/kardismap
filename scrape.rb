#!/usr/bin/ruby

require 'json'
require 'rubygems'
require 'nokogiri'
require 'open-uri'

# add more fields to pull here
descriptors = {'org-name' => 'h1.org-name', 
                'mission' => '#mission .html-snippet', 
                'leadership' => '#ctl00_phMainBody_divQuickLeadership',
                'address1' => '#ctl00_phMainBody_spQuickAddr1',
                'address2' => '#ctl00_phMainBody_spQuickAddr2',
                'url' => '#ctl00_phMainBody_aQuickUrl',
                'type' => '#ctl00_phMainBody_divPrimaryOrganizationSubType'}

def scrape(href, descriptors)
    page =  Nokogiri::HTML(open("http://www.guidestar.org/" + href))
    info = Hash.new
    descriptors.each{ |field, value|
          info[field] = page.css(value).text
    }
    return info
end

ARGV.each do |a|
    myHash = Hash.new
    aFile = File.open(a,"r")
    aFile.each_line{|line|  #intended to read only the first line
        newFile = File.new("data/" + File.basename(a.split('.txt')[0]) + "_data.txt",'w')
        lineinfo = scrape(line, descriptors)
        lineinfo.each { |key, value|
            puts value.strip!
            myHash[key] = value
        }
        newFile.write(JSON.pretty_generate(myHash))
    }
    aFile.close
end
