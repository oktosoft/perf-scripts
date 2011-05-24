# Brett Bates

require 'optparse'
require 'P4'

class TSM2


    def initialize()        
        #Configure
        @root_container = "/Users/brett/p4_work/servers"
        @client_container = "/Users/brett/p4_work/workspaces"
        @p4config_file = "p4config.txt"
        
        @options = {}
    end

    def parse_opts()
        @options[:version] = "20102"
        @options[:port] = "20102"
        @options[:i18n] = false
        @options[:root] = File.join(@root_container, @options[:version])
        @options[:journal] = "journal"
        @options[:log] = "log"
        @options[:client] = "#{@options[:version]}_ws"
        @options[:service] = false
        @options[:daemon] = false
        @options[:user] = "super_test"
        @options[:audit] = nil
        @options[:proxy] = false
        @options[:tunables] = ""
        @options[:server3] = true
        @options[:track1] = true
        

        OptionParser.new do |opts|
            opts.banner = "Usage: tsm.rb [options] -v <UNDELEMITED_VERSION_STRING>"

            opts.on("-v", "--version VERSION", "An undelimited server version e.g 20102") do |v|
                @options[:version] = v
            end

            opts.on("-p", "--port PORT", "Port to run on (DEFAULT:: -v)") do |p|
                @options[:port] = p
            end

            opts.on("-r", "--root PATH", "The servers root") do |r|
                @options[:root] = r
            end

            opts.on("-J", "--journal PATH", "Set the journal file") do |j|
                @options[:journal] = j
            end

            opts.on("-L", "--log PATH", "Set the log file") do |l|
                @options[:log] = l
            end
            
            opts.on("-A", "--audit PATH", "Turn on auditing to file PATH") do |a|
                @options[:audit] = a
            end
            
            opts.on("-P", "--[no-]proxy", "Create a proxy with port -p + 1000") do |p|
                @options[:proxy] = p
            end
            
            opts.on("-t", "--tune", "Extra tuneables") do |t|
                @options[:tuneables] = t
            end
            
            opts.on("-3", "--[no-]3", "Turn on server=3, (on by default)") do |t|
                @options[:server3] = t
            end
            
            opts.on("-1", "--[no-]1", "Turn on track=1, (on by default)") do |o|
                @options[:track1] = o
            end
            
            opts.on("-c", "--client PATH", "Create a client with root PATH") do |w|
                @options[:wlineend] = w
            end            
            
            opts.on("-u", "--user NAME", "Create a use with name NAME") do |u|
                @options[:user] = u
            end
            
            opts.on("-x", "--[no-]i18n", "Turn on i18n") do |x|
                @options[:i18n] = x
            end

            opts.on("-s", "--[no-]service", "Create a windows service") do |s|
                @options[:service] = s
            end
            
            opts.on("-d", "--[no-]daemon", "Make the server a unix daemon") do |d|
                @options[:daemon] = d
            end                 

            opts.on_tail("-h", "--help", "Show this message") do
              puts opts
              exit
            end

        end.parse!(ARGV)

        p @options
    end
    
    def write_config
        File.open(File.join(@client_container, @options[:client], @p4config_file),'w') do |f|
            f.puts("P4PORT=#{@options[:port]}\n")
            f.puts("P4CLIENT=#{@options[:client]}\n")
            f.puts("P4USER=#{@options[:user]}\n")
        end
    end
end

tsm = TSM2.new
tsm.parse_opts