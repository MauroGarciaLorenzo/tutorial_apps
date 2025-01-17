/*
 *  Copyright 2002-2015 Barcelona Supercomputing Center (www.bsc.es)
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */
package hello;


public class Hello {
	
	private static void usage() {
		System.out.println("    Usage: hello.Hello");
	}
	
	public static void main(String[] args) throws Exception {
		// Check and get parameters
		if (args.length != 0) {
			usage();
			throw new Exception("[ERROR] Incorrect number of parameters");
		}
		
		// Hello World from main application
		System.out.println("Hello World! (from main application)");

		// Hello World from a task
		HelloImpl.sayHello();
	}
	
} 
